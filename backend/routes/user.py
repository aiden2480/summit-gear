import uuid
from typing import Optional
from aiohttp import web
from sqlmodel import select
from sqlalchemy import func
from email_validator import validate_email, EmailNotValidError
from database import get_session
from database.models import User
from routes.auth import get_current_user, require_admin, hash_password
from routes.helpers import try_parse_uuid, try_parse_json_body


routes = web.RouteTableDef()


@routes.get("/api/users")
@require_admin
async def get_all_users(request: web.Request) -> web.Response:
    async with get_session() as session:
        result = await session.execute(select(User).order_by(User.username))
        items = result.scalars().all()
        return web.json_response([item.to_dict() for item in items])


def _validate_changes(data: dict, allow_role_change: bool):
    """Validate the request body. Returns (changes, None) on success
    or (None, error_response) on validation failure."""
    new_email = data.get("email")
    new_password = data.get("password")
    new_role = data.get("role")

    if new_role is not None and not allow_role_change:
        return None, web.json_response({"error": "Only admins can change roles"}, status=403)

    if new_role is not None and new_role not in ("user", "admin"):
        return None, web.json_response({"error": "Invalid role"}, status=400)

    if new_password is not None and len(new_password) < 8:
        return None, web.json_response({"error": "Password must be at least 8 characters"}, status=400)

    if new_email is not None:
        new_email = new_email.strip()
        try:
            valid = validate_email(new_email, check_deliverability=False)
            new_email = valid.normalized
        except EmailNotValidError as e:
            return None, web.json_response({"error": f"Invalid email address: {e}"}, status=400)

    if new_email is None and new_password is None and new_role is None:
        return None, web.json_response({"error": "No changes provided"}, status=400)

    return {"email": new_email, "password": new_password, "role": new_role}, None


async def _persist_changes(target_uuid: uuid.UUID, changes: dict) -> web.Response:
    """Load the user by id, apply validated changes, persist, return the JSON response."""

    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        new_email = changes["email"]
        if new_email is not None and new_email.lower() != user.username.lower():
            existing = await session.execute(
                select(User).where(func.lower(User.username) == new_email.lower())
            )
            if existing.scalars().first():
                return web.json_response({"error": "Email already in use"}, status=409)
            user.username = new_email

        if changes["password"] is not None:
            user.hashed_password = hash_password(changes["password"])

        if changes["role"] is not None:
            user.role = changes["role"]

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return web.json_response(user.to_dict())


@routes.put("/api/users/me")
async def update_self(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    data = await try_parse_json_body(request)

    changes, err = _validate_changes(data, allow_role_change=False)
    if err is not None:
        return err

    return await _persist_changes(caller["user_id"], changes)


@routes.put("/api/users/{user_id}")
@require_admin
async def update_user(request: web.Request) -> web.Response:
    target_uuid = try_parse_uuid(request.match_info["user_id"])
    caller = request["user"]
    data = await try_parse_json_body(request)

    changes, err = _validate_changes(data, allow_role_change=True)
    if err is not None:
        return err

    if changes["role"] is not None and caller["user_id"] == target_uuid:
        return web.json_response({"error": "Admins cannot change their own role"}, status=400)

    return await _persist_changes(target_uuid, changes)


@routes.delete("/api/users/{user_id}")
@require_admin
async def delete_user(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
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


# ---------------------------------------------------------------------------
# Avatar handling
# ---------------------------------------------------------------------------

_ALLOWED_AVATAR_MIMES = {"image/png", "image/jpeg"}
_MAX_AVATAR_BYTES = 2 * 1024 * 1024  # 2 MB
_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
_JPEG_MAGIC = b"\xff\xd8\xff"


def _sniff_mime(data: bytes) -> Optional[str]:
    if data.startswith(_PNG_MAGIC):
        return "image/png"
    if data.startswith(_JPEG_MAGIC):
        return "image/jpeg"
    return None


async def _read_avatar_upload(request: web.Request) -> bytes:
    """Parse a multipart upload, validate type + magic bytes + size.
    Returns the validated image bytes or raises an HTTP error response."""
    try:
        reader = await request.multipart()
    except Exception:
        raise web.HTTPBadRequest(text="Expected multipart/form-data")

    field = await reader.next()
    while field is not None and field.name != "file":
        field = await reader.next()
    if field is None:
        raise web.HTTPBadRequest(text="Missing 'file' field")

    declared_mime = (field.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
    if declared_mime not in _ALLOWED_AVATAR_MIMES:
        raise web.HTTPBadRequest(text="Only PNG and JPEG images are allowed")

    buf = bytearray()
    while True:
        chunk = await field.read_chunk(64 * 1024)
        if not chunk:
            break
        buf.extend(chunk)
        if len(buf) > _MAX_AVATAR_BYTES:
            raise web.HTTPRequestEntityTooLarge(
                max_size=_MAX_AVATAR_BYTES, actual_size=len(buf), text="Image must be 2 MB or smaller"
            )

    if not buf:
        raise web.HTTPBadRequest(text="Empty upload")

    sniffed = _sniff_mime(bytes(buf))
    if sniffed is None or sniffed != declared_mime:
        raise web.HTTPBadRequest(text="File contents do not match a PNG or JPEG image")

    return bytes(buf)


async def _persist_avatar(target_uuid: uuid.UUID, data: bytes) -> web.Response:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()
        if not user:
            raise web.HTTPNotFound(text="User not found")
        user.avatar_blob = data
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return web.json_response(user.to_dict())


async def _clear_avatar(target_uuid: uuid.UUID) -> web.Response:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()
        if not user:
            raise web.HTTPNotFound(text="User not found")
        user.avatar_blob = None
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return web.json_response(user.to_dict())


@routes.put("/api/users/me/avatar")
async def upload_self_avatar(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    data = await _read_avatar_upload(request)
    return await _persist_avatar(caller["user_id"], data)


@routes.delete("/api/users/me/avatar")
async def delete_self_avatar(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    return await _clear_avatar(caller["user_id"])


@routes.put("/api/users/{user_id}/avatar")
@require_admin
async def upload_user_avatar(request: web.Request) -> web.Response:
    target_uuid = try_parse_uuid(request.match_info["user_id"])
    data = await _read_avatar_upload(request)
    return await _persist_avatar(target_uuid, data)


@routes.delete("/api/users/{user_id}/avatar")
@require_admin
async def delete_user_avatar(request: web.Request) -> web.Response:
    target_uuid = try_parse_uuid(request.match_info["user_id"])
    return await _clear_avatar(target_uuid)
