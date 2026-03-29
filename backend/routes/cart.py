from aiohttp import web
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from database import get_session
from database.models import CartItem, Product


routes = web.RouteTableDef()


@routes.get("/api/cart")
async def get_cart(request):
    async with get_session() as session:
        result = await session.execute(
            select(CartItem).options(joinedload(CartItem.product)).order_by(CartItem.id)
        )
        items = result.unique().scalars().all()

    return web.json_response([item.to_dict() for item in items])


@routes.post("/api/cart")
async def add_to_cart(request):
    data = await request.json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        raise web.HTTPBadRequest(text="Missing product_id")
    if quantity < 1:
        raise web.HTTPBadRequest(text="Quantity must be at least 1")

    async with get_session() as session:
        # Get product
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar()
        if not product:
            raise web.HTTPNotFound(text="Product not found")

        if product.stock < quantity:
            raise web.HTTPBadRequest(text="Not enough stock available")

        # Check if product already in cart
        result = await session.execute(select(CartItem).where(CartItem.product_id == product_id))
        existing = result.scalar()

        if existing:
            new_qty = existing.quantity + quantity
            if new_qty > product.stock:
                raise web.HTTPBadRequest(text="Not enough stock available")
            existing.quantity = new_qty
        else:
            cart_item = CartItem(product_id=product_id, quantity=quantity)
            session.add(cart_item)

        await session.commit()
        
        # Fetch updated item with product relationship
        result = await session.execute(
            select(CartItem)
            .where(CartItem.product_id == product_id)
            .options(joinedload(CartItem.product))
        )
        item = result.unique().scalar()

    return web.json_response(item.to_dict(), status=201)


@routes.put("/api/cart/{id}")
async def update_cart_item(request):
    item_id = int(request.match_info["id"])
    data = await request.json()
    quantity = data.get("quantity")

    if quantity is None:
        raise web.HTTPBadRequest(text="Missing quantity")
    if quantity < 1:
        raise web.HTTPBadRequest(text="Quantity must be at least 1")

    async with get_session() as session:
        result = await session.execute(
            select(CartItem)
            .where(CartItem.id == item_id)
            .options(joinedload(CartItem.product))
        )
        item = result.unique().scalar()

        if not item:
            raise web.HTTPNotFound(text="Cart item not found")

        if quantity > item.product.stock:
            raise web.HTTPBadRequest(text="Not enough stock available")

        item.quantity = quantity
        await session.commit()
        await session.refresh(item)

    return web.json_response(item.to_dict())


@routes.delete("/api/cart/{id}")
async def remove_from_cart(request):
    item_id = int(request.match_info["id"])
    
    async with get_session() as session:
        result = await session.execute(select(CartItem).where(CartItem.id == item_id))
        item = result.scalar()

        if not item:
            raise web.HTTPNotFound(text="Cart item not found")

        await session.delete(item)
        await session.commit()

    return web.json_response({"message": "Item removed from cart"})


@routes.delete("/api/cart")
async def clear_cart(request):
    async with get_session() as session:
        await session.execute(delete(CartItem))
        await session.commit()

    return web.json_response({"message": "Cart cleared"})


@routes.post("/api/checkout")
async def checkout(request):
    async with get_session() as session:
        # Get all cart items
        result = await session.execute(select(CartItem).options(joinedload(CartItem.product)))
        items = result.unique().scalars().all()

        if not items:
            raise web.HTTPBadRequest(text="Cart is empty")

        # Reduce stock for each item and validate availability
        for item in items:
            if item.product.stock < item.quantity:
                raise web.HTTPBadRequest(text=f"Not enough stock for {item.product.name}")
            item.product.stock -= item.quantity

        # Clear cart
        await session.execute(delete(CartItem))
        await session.commit()

    return web.json_response({"status": "success", "message": "Order placed successfully"})
