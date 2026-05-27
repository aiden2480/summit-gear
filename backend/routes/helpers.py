import json
import uuid
from aiohttp import BodyPartReader, MultipartReader, web

"""
These are a group of helper functions that are used across multiple files, they're defined here to help us follow DRY
"""

def try_parse_uuid(input: str, field: str = "user ID") -> uuid.UUID:
    try:
        return uuid.UUID(input)
    except ValueError:
        raise web.HTTPBadRequest(text=f"Invalid {field}")


def try_parse_int(input: str, field: str = "id") -> int:
    try:
        return int(input)
    except (TypeError, ValueError):
        raise web.HTTPBadRequest(text=f"Invalid {field}")


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
    buffer = bytearray()

    # By reading the packet in chunks, we can determine if it is too large
    # without actually loading the whole packet. This prevents DOS attacks
    # by trying to upload large files
    while chunk := await reader.read_chunk():
        buffer.extend(chunk)

        if len(buffer) > max_size:
            raise web.HTTPRequestEntityTooLarge(max_size, actual_size=len(buffer))

    return bytes(buffer)
