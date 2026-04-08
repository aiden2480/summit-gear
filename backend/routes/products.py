from aiohttp import web
from sqlmodel import select
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


@routes.get("/api/categories")
async def get_categories(request):
    async with get_session() as session:
        result = await session.execute(
            select(Product.category).distinct().order_by(Product.category)
        )
        categories = result.scalars().all()

    return web.json_response(list(categories))
