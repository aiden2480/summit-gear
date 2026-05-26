import uuid
from dataclasses import dataclass
from typing import Optional
from aiohttp import web
from sqlmodel import select
from sqlalchemy import func
from email_validator import validate_email, EmailNotValidError
from database import get_session
from database.models import User
from routes.auth import require_admin, hash_password
from routes.helpers import try_parse_multipart, try_parse_uuid, try_read_bytes


routes = web.RouteTableDef()


@dataclass
class UpdateUserPayload:
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    avatar_data: Optional[bytes] = None
    avatar_mime: Optional[str] = None
    remove_avatar: bool = False


def _validate_changes(payload: UpdateUserPayload, allow_role_change: bool) -> Optional[web.Response]:
    if payload.role is not None and not allow_role_change:
        return web.json_response({"error": "Only admins can change roles"}, status=403)

    if payload.role is not None and payload.role not in ("user", "admin"):
        return web.json_response({"error": "Invalid role"}, status=400)

    if payload.password is not None and len(payload.password) < 8:
        return web.json_response({"error": "Password must be at least 8 characters"}, status=400)

    if payload.email is not None:
        payload.email = payload.email.strip()
        try:
            valid = validate_email(payload.email, check_deliverability=False)
            payload.email = valid.normalized
        except EmailNotValidError as e:
            return web.json_response({"error": f"Invalid email address: {e}"}, status=400)

    return None


_ALLOWED_AVATAR_MIMES = {"image/png", "image/jpeg"}
_MAX_AVATAR_BYTES = 2 * 1024 * 1024


async def _parse_multipart(request: web.Request) -> UpdateUserPayload:
    reader = await try_parse_multipart(request)
    payload = UpdateUserPayload()

    part = await reader.next()
    while part is not None:
        if part.name == "avatar":
            declared_mime = (part.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
            if declared_mime not in _ALLOWED_AVATAR_MIMES:
                raise web.HTTPBadRequest(text="Only PNG and JPEG images are allowed")
            
            data = await try_read_bytes(part, max_size=_MAX_AVATAR_BYTES)

            if not data:
                raise web.HTTPBadRequest(text="Empty upload")
            payload.avatar_data = data
            payload.avatar_mime = declared_mime
        else:
            value = await part.text()
            setattr(payload, part.name, value or None)
        part = await reader.next()

    if payload.remove_avatar:
        payload.avatar_data = None
        payload.avatar_mime = None

    return payload


async def _persist_changes(target_uuid: uuid.UUID, payload: UpdateUserPayload) -> web.Response:
    if not any([payload.email, payload.password, payload.role, payload.avatar_data, payload.remove_avatar]):
        return web.json_response({"error": "No changes provided"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        new_email = payload.email
        if new_email is not None and new_email.lower() != user.username.lower():
            existing = await session.execute(
                select(User).where(func.lower(User.username) == new_email.lower())
            )
            if existing.scalars().first():
                return web.json_response({"error": "Email already in use"}, status=409)
            user.username = new_email

        if payload.password is not None:
            user.hashed_password = hash_password(payload.password)

        if payload.role is not None:
            user.role = payload.role

        if payload.avatar_data is not None:
            user.avatar_data = payload.avatar_data
            user.avatar_mime = payload.avatar_mime
        elif payload.remove_avatar:
            user.avatar_data = None
            user.avatar_mime = None

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return web.json_response(user.to_dict())


@routes.get("/api/users")
@require_admin
async def get_all_users(request: web.Request) -> web.Response:
    async with get_session() as session:
        result = await session.execute(select(User).order_by(User.username))
        items = result.scalars().all()
        return web.json_response([item.to_dict() for item in items])


@routes.put("/api/users/{user_id}")
@require_admin
async def update_user(request: web.Request) -> web.Response:
    target_uuid = try_parse_uuid(request.match_info["user_id"])
    caller = request["user"]
    payload = await _parse_multipart(request)
    err = _validate_changes(payload, allow_role_change=True)
    if err is not None:
        return err
    if payload.role is not None and caller["user_id"] == target_uuid:
        return web.json_response({"error": "Admins cannot change their own role"}, status=400)
    return await _persist_changes(target_uuid, payload)


@routes.delete("/api/users/{user_id}")
@require_admin
async def delete_user(request: web.Request) -> web.Response:
    caller = request["user"]
    target_uuid = try_parse_uuid(request.match_info["user_id"])

    if caller["user_id"] == target_uuid:
        return web.json_response({"error": "Admins cannot delete their own account"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        await session.delete(user)
        await session.commit()

    return web.json_response({"message": "User deleted"})
