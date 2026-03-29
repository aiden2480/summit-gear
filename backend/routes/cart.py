from aiohttp import web
from database import get_db


routes = web.RouteTableDef()


@routes.get("/api/cart")
async def get_cart(request):
    async with get_db() as db:
        db.row_factory = _row_factory
        cursor = await db.execute("""
            SELECT c.id, c.product_id, c.quantity,
                   p.name, p.price, p.image_url, p.stock
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            ORDER BY c.id
        """)
        items = await cursor.fetchall()
    return web.json_response(items)


@routes.post("/api/cart")
async def add_to_cart(request):
    data = await request.json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        raise web.HTTPBadRequest(text="Missing product_id")
    if quantity < 1:
        raise web.HTTPBadRequest(text="Quantity must be at least 1")

    async with get_db() as db:
        db.row_factory = _row_factory
        cursor = await db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = await cursor.fetchone()
        if not product:
            raise web.HTTPNotFound(text="Product not found")

        if product["stock"] < quantity:
            raise web.HTTPBadRequest(text="Not enough stock available")

        cursor = await db.execute(
            "SELECT * FROM cart_items WHERE product_id = ?", (product_id,)
        )
        existing = await cursor.fetchone()

        if existing:
            new_qty = existing["quantity"] + quantity
            if new_qty > product["stock"]:
                raise web.HTTPBadRequest(text="Not enough stock available")
            await db.execute(
                "UPDATE cart_items SET quantity = ? WHERE id = ?",
                (new_qty, existing["id"]),
            )
        else:
            await db.execute(
                "INSERT INTO cart_items (product_id, quantity) VALUES (?, ?)",
                (product_id, quantity),
            )
        await db.commit()

        cursor = await db.execute("""
            SELECT c.id, c.product_id, c.quantity,
                   p.name, p.price, p.image_url, p.stock
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.product_id = ?
        """, (product_id,))
        item = await cursor.fetchone()

    return web.json_response(item, status=201)


@routes.put("/api/cart/{id}")
async def update_cart_item(request):
    item_id = int(request.match_info["id"])
    data = await request.json()
    quantity = data.get("quantity")

    if quantity is None:
        raise web.HTTPBadRequest(text="Missing quantity")
    if quantity < 1:
        raise web.HTTPBadRequest(text="Quantity must be at least 1")

    async with get_db() as db:
        db.row_factory = _row_factory
        cursor = await db.execute("""
            SELECT c.*, p.stock FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.id = ?
        """, (item_id,))
        item = await cursor.fetchone()

        if not item:
            raise web.HTTPNotFound(text="Cart item not found")

        if quantity > item["stock"]:
            raise web.HTTPBadRequest(text="Not enough stock available")

        await db.execute(
            "UPDATE cart_items SET quantity = ? WHERE id = ?",
            (quantity, item_id),
        )
        await db.commit()

        cursor = await db.execute("""
            SELECT c.id, c.product_id, c.quantity,
                   p.name, p.price, p.image_url, p.stock
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.id = ?
        """, (item_id,))
        updated = await cursor.fetchone()

    return web.json_response(updated)


@routes.delete("/api/cart/{id}")
async def remove_from_cart(request):
    item_id = int(request.match_info["id"])
    async with get_db() as db:
        cursor = await db.execute("SELECT id FROM cart_items WHERE id = ?", (item_id,))
        if not await cursor.fetchone():
            raise web.HTTPNotFound(text="Cart item not found")
        await db.execute("DELETE FROM cart_items WHERE id = ?", (item_id,))
        await db.commit()
    return web.json_response({"message": "Item removed from cart"})


@routes.delete("/api/cart")
async def clear_cart(request):
    async with get_db() as db:
        await db.execute("DELETE FROM cart_items")
        await db.commit()
    return web.json_response({"message": "Cart cleared"})


def _row_factory(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
