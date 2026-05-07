import os
import jwt
import bcrypt
from aiohttp import web
from datetime import datetime, timedelta, timezone
from email_validator import validate_email, EmailNotValidError
from sqlmodel import select
from database import get_session
from database.models import User


routes = web.RouteTableDef()

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is not set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


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
    """
    ---
    summary: Login and receive a JWT token
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [username, password]
          properties:
            username:
              type: string
              example: user@example.com
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login successful — returns JWT token
      400:
        description: Invalid email format
      401:
        description: Invalid credentials
    """
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return web.json_response({"error": "Username and password required"}, status=400)

    try:
        validate_email(username, check_deliverability=False)
    except EmailNotValidError as e:
        return web.json_response({"error": f"Invalid email address: {e}"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        return web.json_response({"error": "Invalid credentials"}, status=401)

    token = create_access_token(user.username, user.role)
    return web.json_response({"user": user.username, "token": token, "role": user.role})


@routes.post("/register")
async def register(request: web.Request) -> web.Response:
    """
    ---
    summary: Register a new user account
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [username, password]
          properties:
            username:
              type: string
              example: newuser@example.com
            password:
              type: string
              example: password123
    responses:
      201:
        description: Registration successful — returns JWT token
      400:
        description: Invalid email format or missing fields
      409:
        description: Username already exists
    """
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return web.json_response({"error": "Username and password required"}, status=400)

    if len(password) < 8:
        return web.json_response({"error": "Password must be at least 8 characters"}, status=400)

    try:
        validate_email(username, check_deliverability=False)
    except EmailNotValidError as e:
        return web.json_response({"error": f"Invalid email address: {e}"}, status=400)

    async with get_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        if result.scalars().first():
            return web.json_response({"error": "Username already exists"}, status=409)

        new_user = User(username=username, hashed_password=hash_password(password), role="user")
        session.add(new_user)
        await session.commit()

    token = create_access_token(username, "user")
    return web.json_response({"user": username, "token": token, "role": "user"}, status=201)
