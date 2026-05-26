import json
import uuid
from aiohttp import BodyPartReader, MultipartReader, web

def try_parse_uuid(input: str) -> uuid.UUID:
    try:
        return uuid.UUID(input)
    except ValueError:
        raise web.HTTPBadRequest(text="Invalid user ID")


async def try_parse_json_body(request: web.Request) -> dict:
    try:
        return await request.json()
    except (json.JSONDecodeError, ValueError):
        raise web.HTTPBadRequest(text="Invalid JSON body")


async def try_parse_multipart(request: web.Request) -> MultipartReader:
    try:
        return await request.multipart()
    except Exception:
        raise web.HTTPBadRequest(text="Expected multipart/form-data")


async def try_read_bytes(reader: BodyPartReader, *, max_size: int) -> bytes:
    data = await reader.read_chunk(max_size + 1)

    if len(data) > max_size:
        raise web.HTTPRequestEntityTooLarge(max_size, actual_size=len(data))
    
    return data
