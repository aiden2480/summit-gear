import json
import uuid
from aiohttp import web

def try_parse_uuid(input: str) -> uuid.UUID:
    try:
        return uuid.UUID(input)
    except ValueError:
        raise web.HTTPBadRequest(text="Invalid user ID")


async def parse_json_body(request: web.Request) -> dict:
    try:
        return await request.json()
    except (json.JSONDecodeError, ValueError):
        raise web.HTTPBadRequest(text="Invalid JSON body")
