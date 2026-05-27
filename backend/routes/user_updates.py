"""Shared logic for updating a user record.
"""

import uuid
from dataclasses import dataclass
from typing import Optional
from aiohttp import web
from sqlmodel import select
from sqlalchemy import func
from email_validator import validate_email, EmailNotValidError
from database import get_session
from database.models import User
from routes.helpers import try_parse_multipart, try_read_bytes


_ALLOWED_AVATAR_MIMES = {"image/png", "image/jpeg"}
_MAX_AVATAR_BYTES = 2 * 1024 * 1024


@dataclass
class UpdateUserPayload:
    """Edit payload: only updates the fields the caller filled in."""
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    avatar_data: Optional[bytes] = None
    avatar_mime: Optional[str] = None
    remove_avatar: bool = False

    @property
    def is_empty(self):
        """If the request body was empty, no changes were requested from the caller"""
        return not any([self.email, self.password, self.role, self.avatar_data, self.avatar_mime, self.remove_avatar])


# helper function to enusre that all of the information for a user update request is correct and makes sense from a business perspective
def validate_changes(payload: UpdateUserPayload, allow_role_change: bool) -> Optional[web.Response]:
    """Validate email/password/role fields. allow_role_change=False stops users promoting themselves."""
    if payload.role is not None and not allow_role_change:
        return web.Response(text="Only admins can change roles", status=403)

    if payload.role is not None and payload.role not in ("user", "admin"):
        return web.Response(text="Invalid role", status=400)

    if payload.password is not None and len(payload.password) < 8:
        return web.Response(text="Password must be at least 8 characters", status=400)

    if payload.email is not None:
        payload.email = payload.email.strip()
        try:
            valid = validate_email(payload.email, check_deliverability=False)
            payload.email = valid.normalized
        except EmailNotValidError as e:
            return web.Response(text=f"Invalid email address: {e}", status=400)

    return None


async def parse_multipart(request: web.Request) -> UpdateUserPayload:
    """Parse the multipart form into an UpdateUserPayload."""
    reader = await try_parse_multipart(request)
    data: dict = {}

    while (part := await reader.next()) is not None:
        if part.name != "avatar":
            data[part.name] = await part.text()
            continue

        mime = part.headers.get("Content-Type", "")

        if mime not in _ALLOWED_AVATAR_MIMES:
            raise web.HTTPBadRequest(text=f"Mime {mime} is not permitted for avatar upload")

        data["avatar_data"] = await try_read_bytes(part, max_size=_MAX_AVATAR_BYTES)
        data["avatar_mime"] = mime

    payload = UpdateUserPayload(
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role"),
        avatar_data=data.get("avatar_data"),
        avatar_mime=data.get("avatar_mime"),
        remove_avatar=data.get("remove_avatar", "").lower() == "true",
    )

    if payload.remove_avatar:
        payload.avatar_data = None
        payload.avatar_mime = None

    return payload


async def persist_changes(target_uuid: uuid.UUID, payload: UpdateUserPayload) -> web.Response:
    """Write the payload fields to the target user."""
    # Local import to avoid a circular import: routes.auth imports nothing from
    # this module, but importing hash_password at module level would create a
    # cycle through routes.admin -> routes.auth -> routes.helpers in some setups.
    from routes.auth import hash_password

    if payload.is_empty:
        return web.Response(text="No changes provided", status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == target_uuid))
        user = result.scalars().first()

        if not user:
            raise web.HTTPNotFound(text="User not found")

        new_email = payload.email
        if new_email is not None and new_email.lower() != user.username.lower():
            existing = await session.execute(
                select(User).where(func.lower(User.username) == new_email.lower())
            )
            if existing.scalars().first():
                return web.Response(text="Email already in use", status=409)
            user.username = new_email

        if payload.password is not None:
            user.hashed_password = hash_password(payload.password)

        if payload.role is not None:
            user.role = payload.role

        if payload.avatar_data is not None:
            user.avatar_data = payload.avatar_data
            user.avatar_mime = payload.avatar_mime
        elif payload.remove_avatar:
            user.avatar_data = None
            user.avatar_mime = None

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return web.json_response(user.to_dict())
