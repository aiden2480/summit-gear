import os
import jwt
from aiohttp import web
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlmodel import select
from database import get_session
from database.models import User


routes = web.RouteTableDef()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "summit-gear-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


def create_access_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "role": role, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: web.Request) -> dict:
    """Extract and verify JWT from the Authorization header. Returns {"username": ..., "role": ...}."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise web.HTTPUnauthorized(text="Missing or invalid authorization header")
    token = auth_header[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role", "user")
        if not username:
            raise web.HTTPUnauthorized(text="Invalid token payload")
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise web.HTTPUnauthorized(text="Token has expired")
    except jwt.PyJWTError:
        raise web.HTTPUnauthorized(text="Could not validate credentials")


async def require_admin(request: web.Request) -> dict:
    """Like get_current_user but raises 403 if the user is not an admin."""
    user = await get_current_user(request)
    if user["role"] != "admin":
        raise web.HTTPForbidden(text="Admin access required")
    return user


@routes.post("/login")
async def login(request: web.Request) -> web.Response:
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return web.json_response({"error": "Username and password required"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()

    if not user or not pwd_context.verify(password, user.hashed_password):
        return web.json_response({"error": "Invalid credentials"}, status=401)

    token = create_access_token(user.username, user.role)
    return web.json_response({"user": user.username, "token": token, "role": user.role})


@routes.post("/register")
async def register(request: web.Request) -> web.Response:
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return web.json_response({"error": "Username and password required"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        if result.scalars().first():
            return web.json_response({"error": "Username already exists"}, status=409)

        new_user = User(username=username, hashed_password=pwd_context.hash(password), role="user")
        session.add(new_user)
        await session.commit()

    token = create_access_token(username, "user")
    return web.json_response({"user": username, "token": token, "role": "user"}, status=201)
