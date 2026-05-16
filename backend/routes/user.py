from aiohttp import web
from sqlmodel import select
from database import get_session
from database.models import User
from routes.auth import get_current_user

routes = web.RouteTableDef()

@routes.get("/api/users")
async def get_all_users(request: web.Request) -> web.Response:
    async with get_session() as session:
        role = (await get_current_user(request)).get("role", "")

        if (role != "admin") : 
            raise web.HTTPUnauthorized(text="User list is only avaliable for admins")
        result = await session.execute(select(User).order_by(User.id))

        items = result.scalars().all()

        return web.json_response([item.to_dict() for item in items])
