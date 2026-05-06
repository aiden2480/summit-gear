import aiohttp_cors
from aiohttp import web
from database import init_db
from routes.auth import routes as auth_routes
from routes.cart import routes as cart_routes
from routes.products import routes as product_routes


def create_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(init_db)

    app.router.add_routes(auth_routes)
    app.router.add_routes(product_routes)
    app.router.add_routes(cart_routes)

    # Enable CORS so the frontend (localhost:5173) can make requests to the
    # backend (localhost:8080). Without this, browsers block cross-origin fetches.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8080)
