import uuid
from aiohttp import web
from sqlmodel import select
from sqlalchemy.orm import joinedload
from database import get_session
from database.models import User, CartItem
from routes.auth import require_admin
from routes.helpers import try_parse_uuid
from routes.user_updates import parse_multipart, persist_changes, validate_changes


routes = web.RouteTableDef()


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
    payload = await parse_multipart(request)
    err = validate_changes(payload, allow_role_change=True)
    if err is not None:
        return err
    if payload.role is not None and caller["user_id"] == target_uuid:
        return web.Response(text="Admins cannot change their own role", status=400)
    return await persist_changes(target_uuid, payload)


@routes.delete("/api/users/{user_id}")
@require_admin
async def delete_user(request: web.Request) -> web.Response:
    caller = request["user"]
    target_uuid = try_parse_uuid(request.match_info["user_id"])

    if caller["user_id"] == target_uuid:
        return web.Response(text="Admins cannot delete their own account", status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        await session.delete(user)
        await session.commit()

    return web.json_response({"message": "User deleted"})


@routes.get("/api/cart/user/{user_id}")
@require_admin
async def get_user_cart(request: web.Request) -> web.Response:
    """Return the cart items belonging to any user. Admin only."""
    target_uuid = try_parse_uuid(request.match_info["user_id"])
    async with get_session() as session:
        result = await session.execute(
            select(CartItem)
            .where(CartItem.user_id == target_uuid)
            .options(joinedload(CartItem.product))
            .order_by(CartItem.id)
        )
        items = result.unique().scalars().all()
        return web.json_response([item.to_dict() for item in items])
