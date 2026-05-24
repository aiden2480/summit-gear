import json
import uuid
from aiohttp import web
from sqlmodel import select
from sqlalchemy import func
from email_validator import validate_email, EmailNotValidError
from database import get_session
from database.models import User
from routes.auth import get_current_user, require_admin, hash_password


routes = web.RouteTableDef()


@routes.get("/api/users")
@require_admin
async def get_all_users(request: web.Request) -> web.Response:
    async with get_session() as session:
        result = await session.execute(select(User).order_by(User.username))
        items = result.scalars().all()
        return web.json_response([item.to_dict() for item in items])


@routes.put("/api/users/{user_id}")
async def update_user(request: web.Request) -> web.Response:
    target_user_id = request.match_info["user_id"]
    caller = await get_current_user(request)

    is_admin = caller["role"] == "admin"
    is_self = str(caller["user_id"]) == target_user_id

    if not is_admin and not is_self:
        raise web.HTTPForbidden(text="You can only edit your own account")

    try:
        data = await request.json()
    except (json.JSONDecodeError, ValueError):
        raise web.HTTPBadRequest(text="Invalid JSON body")

    new_email = data.get("email")
    new_password = data.get("password")
    new_role = data.get("role")

    if new_role is not None and not is_admin:
        raise web.HTTPForbidden(text="Only admins can change roles")

    if new_role is not None and is_self:
        return web.json_response({"error": "Admins cannot change their own role"}, status=400)

    if new_role is not None and new_role not in ("user", "admin"):
        return web.json_response({"error": "Invalid role"}, status=400)

    if new_password is not None and len(new_password) < 8:
        return web.json_response({"error": "Password must be at least 8 characters"}, status=400)

    if new_email is not None:
        new_email = new_email.strip()
        try:
            valid = validate_email(new_email, check_deliverability=False)
            new_email = valid.normalized
        except EmailNotValidError as e:
            return web.json_response({"error": f"Invalid email address: {e}"}, status=400)

    if new_email is None and new_password is None and new_role is None:
        return web.json_response({"error": "No changes provided"}, status=400)

    try:
        target_uuid = uuid.UUID(target_user_id)
    except ValueError:
        raise web.HTTPBadRequest(text="Invalid user ID")

    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        if new_email is not None and new_email.lower() != user.username.lower():
            existing = await session.execute(
                select(User).where(func.lower(User.username) == new_email.lower())
            )
            if existing.scalars().first():
                return web.json_response({"error": "Email already in use"}, status=409)
            user.username = new_email

        if new_password is not None:
            user.hashed_password = hash_password(new_password)

        if new_role is not None:
            user.role = new_role

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return web.json_response(user.to_dict())


@routes.delete("/api/users/{user_id}")
@require_admin
async def delete_user(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    target_user_id = request.match_info["user_id"]

    if str(caller["user_id"]) == target_user_id:
        return web.json_response({"error": "Admins cannot delete their own account"}, status=400)

    try:
        target_uuid = uuid.UUID(target_user_id)
    except ValueError:
        raise web.HTTPBadRequest(text="Invalid user ID")

    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        await session.delete(user)
        await session.commit()

    return web.json_response({"message": "User deleted"})
