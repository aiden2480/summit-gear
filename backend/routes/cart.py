from aiohttp import web
from sqlmodel import select, delete
from sqlalchemy.orm import joinedload
from database import get_session
from database.models import CartItem, Product
from routes.auth import get_current_user
from routes.helpers import try_parse_uuid, try_parse_int, try_parse_json_body

routes = web.RouteTableDef()

@routes.get("/api/cart")
async def get_cart(request: web.Request):
    async with get_session() as session:
        user_id = (await get_current_user(request)).get("user_id", "")
        result = await session.execute(
            select(CartItem).where(CartItem.user_id == user_id).options(joinedload(CartItem.product)).order_by(CartItem.id)
        )
        items = result.unique().scalars().all()

    return web.json_response([item.to_dict() for item in items])


@routes.post("/api/cart")
async def add_to_cart(request: web.Request):
    data = await try_parse_json_body(request)
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        raise web.HTTPBadRequest(text="Missing product_id")
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise web.HTTPBadRequest(text="Quantity must be an integer")
    if quantity < 1:
        raise web.HTTPBadRequest(text="Quantity must be at least 1")

    async with get_session() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        current_user_id = (await get_current_user(request)).get("user_id", "")
        product = result.scalar()
        if not product:
            raise web.HTTPNotFound(text="Product not found")

        if product.stock < quantity:
            raise web.HTTPBadRequest(text="Not enough stock available")

        # Check if product already in cart
        query = select(CartItem).where(CartItem.product_id == product_id, CartItem.user_id == current_user_id)
        result = await session.execute(query)
        existing = result.scalar()

        if existing:
            new_qty = existing.quantity + quantity
            if new_qty > product.stock:
                raise web.HTTPBadRequest(text="Not enough stock available")
            existing.quantity = new_qty
        else:
            cart_item = CartItem(product_id=product_id, quantity=quantity, user_id=current_user_id)
            session.add(cart_item)

        await session.commit()
        
        # Fetch updated item with product relationship
        result = await session.execute(
            select(CartItem)
            .where(CartItem.product_id == product_id, CartItem.user_id == current_user_id)
            .options(joinedload(CartItem.product))
        )
        item = result.unique().scalar()

    return web.json_response(item.to_dict(), status=201)


@routes.put("/api/cart/{id}")
async def update_cart_item(request: web.Request):
    item_id = try_parse_int(request.match_info["id"], field="cart item id")
    data = await try_parse_json_body(request)
    quantity = data.get("quantity")

    if quantity is None:
        raise web.HTTPBadRequest(text="Missing quantity")
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise web.HTTPBadRequest(text="Quantity must be an integer")
    if quantity < 1:
        raise web.HTTPBadRequest(text="Quantity must be at least 1")

    async with get_session() as session:
        current_user_id = (await get_current_user(request)).get("user_id", "")
        result = await session.execute(
            select(CartItem)
            .where(CartItem.id == item_id, CartItem.user_id == current_user_id)
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
async def remove_from_cart(request: web.Request):
    item_id = try_parse_int(request.match_info["id"], field="cart item id")
    
    async with get_session() as session:
        current_user_id = (await get_current_user(request)).get("user_id", "")
        result = await session.execute(select(CartItem).where(CartItem.id == item_id, CartItem.user_id == current_user_id))
        item = result.scalar()

        if not item:
            raise web.HTTPNotFound(text="Cart item not found")

        statement = delete(CartItem).where(CartItem.id == item_id, CartItem.user_id == current_user_id)
        await session.execute(statement)
        await session.commit()

    return web.json_response({"message": "Item removed from cart"})


@routes.delete("/api/cart")
async def clear_cart(request: web.Request):
    async with get_session() as session:
        current_user_id = (await get_current_user(request)).get("user_id", "")
        statement = delete(CartItem).where(CartItem.user_id == current_user_id)
        await session.execute(statement)
        await session.commit()

    return web.json_response({"message": "Cart cleared"})


@routes.post("/api/checkout")
async def checkout(request: web.Request):
    """Atomically validates stock, reduces quantities, and clears the cart."""

    async with get_session() as session:
        current_user_id = (await get_current_user(request)).get("user_id", "")
        result = await session.execute(select(CartItem).where(CartItem.user_id == current_user_id).options(joinedload(CartItem.product)))
        items = result.unique().scalars().all()

        if not items:
            raise web.HTTPBadRequest(text="Cart is empty")

        for item in items:
            if item.product.stock < item.quantity:
                raise web.HTTPBadRequest(text=f"Not enough stock for {item.product.name}")
            item.product.stock -= item.quantity

        statement = delete(CartItem).where(CartItem.user_id == current_user_id)
        await session.execute(statement)
        await session.commit()

    return web.json_response({"status": "success", "message": "Order placed successfully"})

@routes.get("/api/cart/user/{user_id}")
async def get_user_cart(request: web.Request) -> web.Response:
    async with get_session() as session:
        cartitem_user_id = try_parse_uuid(request.match_info["user_id"])

        role = (await get_current_user(request)).get("role", "")

        if role != "admin":
            raise web.HTTPForbidden(text="You are not authorised to perform this action.")

        result = await session.execute(
            select(CartItem).where(CartItem.user_id == cartitem_user_id).options(joinedload(CartItem.product)).order_by(CartItem.id)
        )
        items = result.unique().scalars().all()

        return web.json_response([item.to_dict() for item in items])

