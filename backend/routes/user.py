from typing import Optional
from aiohttp import web
from routes.auth import get_current_user
from routes.helpers import try_parse_json_body, try_parse_uuid
from routes.admin import _validate_changes, _persist_changes


routes = web.RouteTableDef()


@routes.get("/api/users")
@require_admin
async def get_all_users(request: web.Request) -> web.Response:
    async with get_session() as session:
        result = await session.execute(select(User).order_by(User.username))
        items = result.scalars().all()
        return web.json_response([item.to_dict() for item in items])


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


async def _parse_multipart(request: web.Request) -> tuple[dict, Optional[bytes], Optional[str], bool]:
    """Read a multipart update request.

    Returns ``(fields, avatar_data, avatar_mime, remove_avatar)`` where:
    - ``fields`` contains any text parts (email, password, role)
    - ``avatar_data`` / ``avatar_mime`` are set when a valid file part was provided
    - ``remove_avatar`` is True when the ``remove_avatar`` text part equals "true"
    """
    try:
        reader = await request.multipart()
    except Exception:
        raise web.HTTPBadRequest(text="Expected multipart/form-data")

    fields: dict = {}
    avatar_data: Optional[bytes] = None
    avatar_mime: Optional[str] = None
    remove_avatar = False

    field = await reader.next()
    while field is not None:
        if field.name == "avatar":
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
            avatar_data = bytes(buf)
            avatar_mime = sniffed
        else:
            value = await field.text()
            fields[field.name] = value
        field = await reader.next()

    if fields.get("remove_avatar", "").lower() == "true":
        remove_avatar = True
        avatar_data = None
        avatar_mime = None

    return fields, avatar_data, avatar_mime, remove_avatar


def _validate_changes(data: dict, allow_role_change: bool):
    """Validate text fields. Returns (changes, None) on success
    or (None, error_response) on validation failure."""
    new_email = data.get("email") or None
    new_password = data.get("password") or None
    new_role = data.get("role") or None

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

    return {"email": new_email, "password": new_password, "role": new_role}, None


async def _persist_changes(
    target_uuid: uuid.UUID,
    changes: dict,
    avatar_data: Optional[bytes] = None,
    avatar_mime: Optional[str] = None,
    remove_avatar: bool = False,
) -> web.Response:
    if (
        changes["email"] is None
        and changes["password"] is None
        and changes["role"] is None
        and avatar_data is None
        and not remove_avatar
    ):
        return web.json_response({"error": "No changes provided"}, status=400)

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

        if avatar_data is not None:
            user.avatar_data = avatar_data
            user.avatar_mime = avatar_mime
        elif remove_avatar:
            user.avatar_data = None
            user.avatar_mime = None

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return web.json_response(user.to_dict())


@routes.put("/api/users/me")
async def update_self(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    fields, avatar_data, avatar_mime, remove_avatar = await _parse_multipart(request)
    changes, err = _validate_changes(fields, allow_role_change=False)
    if err is not None:
        return err
    return await _persist_changes(caller["user_id"], changes, avatar_data, avatar_mime, remove_avatar)


@routes.put("/api/users/{user_id}")
@require_admin
async def update_user(request: web.Request) -> web.Response:
    target_uuid = try_parse_uuid(request.match_info["user_id"])
    caller = request["user"]
    fields, avatar_data, avatar_mime, remove_avatar = await _parse_multipart(request)
    changes, err = _validate_changes(fields, allow_role_change=True)
    if err is not None:
        return err
    if changes["role"] is not None and caller["user_id"] == target_uuid:
        return web.json_response({"error": "Admins cannot change their own role"}, status=400)
    return await _persist_changes(target_uuid, changes, avatar_data, avatar_mime, remove_avatar)


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
