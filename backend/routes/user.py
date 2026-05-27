from aiohttp import web
from routes.auth import get_current_user
from routes.user_updates import parse_multipart, persist_changes, validate_changes


routes = web.RouteTableDef()


@routes.put("/api/users/me")
async def update_self(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    payload = await parse_multipart(request)
    err = validate_changes(payload, allow_role_change=False)
    if err is not None:
        return err
    return await persist_changes(caller["user_id"], payload)
