import os
import sys
from aiohttp import web
import aiohttp_cors

sys.path.insert(0, os.path.dirname(__file__))

from database import init_db
from routes.products import routes as product_routes
from routes.cart import routes as cart_routes


async def on_startup(app):
    await init_db()


def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)

    app.router.add_routes(product_routes)
    app.router.add_routes(cart_routes)

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
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8080)
