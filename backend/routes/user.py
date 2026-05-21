from aiohttp import web
from sqlmodel import select
from database import get_session
from database.models import User
from routes.auth import get_current_user, require_admin, hash_password


routes = web.RouteTableDef()


@routes.get("/api/users")
@require_admin
async def get_all_users(request: web.Request) -> web.Response:
    async with get_session() as session:
        result = await session.execute(select(User).order_by(User.id))
        items = result.scalars().all()
        return web.json_response([item.to_dict() for item in items])


@routes.put("/api/users/{username}")
async def update_user(request: web.Request) -> web.Response:
    target_username = request.match_info["username"]
    caller = await get_current_user(request)

    is_admin = caller["role"] == "admin"
    is_self = caller["username"] == target_username

    if not is_admin and not is_self:
        raise web.HTTPForbidden(text="You can only edit your own account")

    data = await request.json()

    if "username" in data:
        return web.json_response({"error": "Username changes are not supported"}, status=400)

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

    if new_password is None and new_role is None:
        return web.json_response({"error": "No changes provided"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.username == target_username))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        if new_password is not None:
            user.hashed_password = hash_password(new_password)

        if new_role is not None:
            user.role = new_role

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return web.json_response(user.to_dict())


@routes.delete("/api/users/{username}")
@require_admin
async def delete_user(request: web.Request) -> web.Response:
    caller = request["user"]
    target_username = request.match_info["username"]

    if caller["username"] == target_username:
        return web.json_response({"error": "Admins cannot delete their own account"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.username == target_username))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        await session.delete(user)
        await session.commit()

    return web.json_response({"message": "User deleted"})
