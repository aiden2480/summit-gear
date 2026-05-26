from aiohttp import web
from routes.auth import get_current_user
from routes.admin import _validate_changes, _persist_changes, _parse_multipart


routes = web.RouteTableDef()


@routes.put("/api/users/me")
async def update_self(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    payload = await _parse_multipart(request)
    err = _validate_changes(payload, allow_role_change=False)
    if err is not None:
        return err
    return await _persist_changes(caller["user_id"], payload)
