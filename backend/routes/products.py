from aiohttp import web
from sqlalchemy import select, delete
from database import get_session
from database.models import Product, CartItem


routes = web.RouteTableDef()


@routes.get("/api/products")
async def get_products(request):
    category = request.query.get("category")
    search = request.query.get("search")

    async with get_session() as session:
        query = select(Product)
        
        if category and category != "All":
            query = query.where(Product.category == category)
        if search:
            query = query.where(
                (Product.name.ilike(f"%{search}%")) | 
                (Product.description.ilike(f"%{search}%"))
            )
        
        query = query.order_by(Product.id)
        result = await session.execute(query)
        products = result.scalars().all()

    return web.json_response([p.to_dict() for p in products])


@routes.get("/api/products/{id}")
async def get_product(request):
    product_id = int(request.match_info["id"])
    async with get_session() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar()
    
    if not product:
        raise web.HTTPNotFound(text="Product not found")
    return web.json_response(product.to_dict())


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

    product = Product(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image_url=data["image_url"],
        category=data["category"],
        stock=int(data["stock"]),
    )

    async with get_session() as session:
        session.add(product)
        await session.commit()
        await session.refresh(product)

    return web.json_response(product.to_dict(), status=201)


@routes.put("/api/products/{id}")
async def update_product(request):
    product_id = int(request.match_info["id"])
    data = await request.json()

    async with get_session() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar()

        if not product:
            raise web.HTTPNotFound(text="Product not found")

        for field in ["name", "description", "price", "image_url", "category", "stock"]:
            if field in data:
                setattr(product, field, data[field])

        await session.commit()
        await session.refresh(product)

    return web.json_response(product.to_dict())


@routes.delete("/api/products/{id}")
async def delete_product(request):
    product_id = int(request.match_info["id"])
    
    async with get_session() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar()

        if not product:
            raise web.HTTPNotFound(text="Product not found")

        await session.execute(delete(CartItem).where(CartItem.product_id == product_id))
        await session.delete(product)
        await session.commit()

    return web.json_response({"message": "Product deleted"})


@routes.get("/api/categories")
async def get_categories(request):
    async with get_session() as session:
        result = await session.execute(
            select(Product.category).distinct().order_by(Product.category)
        )
        categories = result.scalars().all()

    return web.json_response(list(categories))
