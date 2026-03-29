from aiohttp import web
from models.database import get_db


routes = web.RouteTableDef()


@routes.get("/api/products")
async def get_products(request):
    category = request.query.get("category")
    search = request.query.get("search")

    query = "SELECT * FROM products"
    params = []
    conditions = []

    if category and category != "All":
        conditions.append("category = ?")
        params.append(category)
    if search:
        conditions.append("(name LIKE ? OR description LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id"

    async with get_db() as db:
        db.row_factory = _row_factory
        cursor = await db.execute(query, params)
        products = await cursor.fetchall()
    return web.json_response(products)


@routes.get("/api/products/{id}")
async def get_product(request):
    product_id = int(request.match_info["id"])
    async with get_db() as db:
        db.row_factory = _row_factory
        cursor = await db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = await cursor.fetchone()
    if not product:
        raise web.HTTPNotFound(text="Product not found")
    return web.json_response(product)


@routes.post("/api/products")
async def create_product(request):
    data = await request.json()
    required = ["name", "description", "price", "image_url", "category", "stock"]
    for field in required:
        if field not in data:
            raise web.HTTPBadRequest(text=f"Missing field: {field}")

    if not data["name"].strip():
        raise web.HTTPBadRequest(text="Product name cannot be empty")
    if data["price"] <= 0:
        raise web.HTTPBadRequest(text="Price must be greater than 0")
    if data["stock"] < 0:
        raise web.HTTPBadRequest(text="Stock cannot be negative")

    async with get_db() as db:
        cursor = await db.execute(
            "INSERT INTO products (name, description, price, image_url, category, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (data["name"], data["description"], float(data["price"]), data["image_url"], data["category"], int(data["stock"])),
        )
        await db.commit()
        product_id = cursor.lastrowid

        db.row_factory = _row_factory
        cursor = await db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = await cursor.fetchone()

    return web.json_response(product, status=201)


@routes.put("/api/products/{id}")
async def update_product(request):
    product_id = int(request.match_info["id"])
    data = await request.json()

    async with get_db() as db:
        cursor = await db.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not await cursor.fetchone():
            raise web.HTTPNotFound(text="Product not found")

        fields = []
        values = []
        for field in ["name", "description", "price", "image_url", "category", "stock"]:
            if field in data:
                fields.append(f"{field} = ?")
                values.append(data[field])

        if not fields:
            raise web.HTTPBadRequest(text="No fields to update")

        values.append(product_id)
        await db.execute(f"UPDATE products SET {', '.join(fields)} WHERE id = ?", values)
        await db.commit()

        db.row_factory = _row_factory
        cursor = await db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = await cursor.fetchone()

    return web.json_response(product)


@routes.delete("/api/products/{id}")
async def delete_product(request):
    product_id = int(request.match_info["id"])
    async with get_db() as db:
        cursor = await db.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not await cursor.fetchone():
            raise web.HTTPNotFound(text="Product not found")
        await db.execute("DELETE FROM cart_items WHERE product_id = ?", (product_id,))
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.commit()
    return web.json_response({"message": "Product deleted"})


@routes.get("/api/categories")
async def get_categories(request):
    async with get_db() as db:
        cursor = await db.execute("SELECT DISTINCT category FROM products ORDER BY category")
        rows = await cursor.fetchall()
    categories = [row[0] for row in rows]
    return web.json_response(categories)


def _row_factory(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
