from aiohttp import web
from routes.auth import get_current_user
from routes.helpers import try_parse_json_body
from routes.admin import _validate_changes, _persist_changes


routes = web.RouteTableDef()


@routes.put("/api/users/me")
async def update_self(request: web.Request) -> web.Response:
    caller = await get_current_user(request)
    data = await try_parse_json_body(request)

    changes, err = _validate_changes(data, allow_role_change=False)
    if err is not None:
        return err

    return await _persist_changes(caller["user_id"], changes)
