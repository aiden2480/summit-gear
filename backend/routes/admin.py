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

    @property
    def is_empty(self):
        """If the request body was empty, no changes were requested from the caller"""
        return not any([self.email, self.password, self.role, self.avatar_data, self.avatar_mime, self.remove_avatar])


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
    data: dict = {}

    while (part := await reader.next()) is not None:
        if part.name != "avatar":
            data[part.name] = await part.text()
            continue

        mime = part.headers.get("Content-Type", "")

        if mime not in _ALLOWED_AVATAR_MIMES:
            raise web.HTTPBadRequest(text=f"Mime {mime} is not permitted for avatar upload")

        data["avatar_data"] = await try_read_bytes(part, max_size=_MAX_AVATAR_BYTES)
        data["avatar_mime"] = mime

    payload = UpdateUserPayload(
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role"),
        avatar_data=data.get("avatar_data"),
        avatar_mime=data.get("avatar_mime"),
        remove_avatar=data.get("remove_avatar", "").lower() == "true",
    )

    if payload.remove_avatar:
        payload.avatar_data = None
        payload.avatar_mime = None

    return payload


async def _persist_changes(target_uuid: uuid.UUID, payload: UpdateUserPayload) -> web.Response:
    if payload.is_empty:
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
