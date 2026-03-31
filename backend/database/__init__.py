import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from database.models import Base, Product

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shop.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db(*_):
    """Initialize database and seed with data"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed data if no products exist
    async with async_session() as session:
        result = await session.execute(select(Product))
        if not result.scalars().first():
            await seed_data(session)


async def seed_data(session: AsyncSession):
    """Seed the database with initial product data"""
    products_data = [
        {
            "name": "Wireless Bluetooth Headphones",
            "description": "Premium noise-cancelling wireless headphones with 30-hour battery life and comfortable over-ear design.",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 25,
        },
        {
            "name": "Organic Cotton T-Shirt",
            "description": "Soft and breathable 100% organic cotton t-shirt available in multiple colours. Ethically sourced.",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
            "category": "Clothing",
            "stock": 50,
        },
        {
            "name": "Stainless Steel Water Bottle",
            "description": "Double-wall insulated 750ml water bottle. Keeps drinks cold for 24 hours or hot for 12 hours.",
            "price": 24.95,
            "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 40,
        },
        {
            "name": "Mechanical Keyboard",
            "description": "RGB backlit mechanical keyboard with Cherry MX Blue switches and aluminium frame.",
            "price": 119.0,
            "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 15,
        },
        {
            "name": "Running Shoes",
            "description": "Lightweight and responsive running shoes with cushioned sole and breathable mesh upper.",
            "price": 74.5,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
            "category": "Clothing",
            "stock": 30,
        },
        {
            "name": "Ceramic Coffee Mug Set",
            "description": "Set of 4 handcrafted ceramic coffee mugs in earthy tones. Microwave and dishwasher safe.",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 20,
        },
        {
            "name": "Portable Power Bank",
            "description": "20000mAh portable charger with fast charging support and dual USB-C ports.",
            "price": 45.0,
            "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 35,
        },
        {
            "name": "Yoga Mat",
            "description": "Non-slip eco-friendly yoga mat with alignment lines. 6mm thick for extra comfort.",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop",
            "category": "Sports",
            "stock": 22,
        },
        {
            "name": "LED Desk Lamp",
            "description": "Adjustable LED desk lamp with 5 brightness levels, 3 colour temperatures, and USB charging port.",
            "price": 42.0,
            "image_url": "https://images.unsplash.com/photo-1621447980929-6638614633c8?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 18,
        },
        {
            "name": "Canvas Backpack",
            "description": "Durable canvas backpack with padded laptop compartment and water-resistant coating.",
            "price": 54.99,
            "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop",
            "category": "Accessories",
            "stock": 28,
        },
        {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with silent click and adjustable DPI up to 4000.",
            "price": 27.5,
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 45,
        },
        {
            "name": "Scented Candle Set",
            "description": "Luxury soy wax candle set with lavender, vanilla, and eucalyptus fragrances. 40-hour burn time each.",
            "price": 32.0,
            "image_url": "https://plus.unsplash.com/premium_photo-1681412205205-5422a084e717?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 33,
        },
        {
            "name": "Winter Beanie",
            "description": "Warm knitted beanie with fleece lining in various colours. One size fits all.",
            "price": 18.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1672883552656-be33f579fc4b?w=400&h=400&fit=crop",
            "category": "Clothing",
            "stock": 55,
        },
        {
            "name": "Stainless Steel Thermos",
            "description": "Keeps beverages hot for 12 hours or cold for 24 hours. Leak-proof lid and ergonomic handle.",
            "price": 35.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1681154819809-b660a509e1ee?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 26,
        },
        {
            "name": "USB-C Fast Charger",
            "description": "65W USB-C PD charger supporting multiple devices simultaneously. Compact design for travel.",
            "price": 38.5,
            "image_url": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 42,
        },
        {
            "name": "Sports Water Bottle",
            "description": "1L sports bottle with time markers and leak-proof flip cap. BPA-free plastic.",
            "price": 16.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1674440623489-5d7cac56bc0f?w=400&h=400&fit=crop",
            "category": "Sports",
            "stock": 60,
        },
        {
            "name": "Desk Organizer Set",
            "description": "5-piece bamboo desk organizer set including pen holder, paper tray, and drawer dividers.",
            "price": 29.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1683543124636-518d6c09751f?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 31,
        },
        {
            "name": "Phone Stand",
            "description": "Adjustable aluminum phone stand for desk. Compatible with all smartphones and small tablets.",
            "price": 14.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1680623396167-a5f265a2fd49?w=400&h=400&fit=crop",
            "category": "Accessories",
            "stock": 48,
        },
        {
            "name": "Fitness Resistance Bands",
            "description": "Set of 5 color-coded resistance bands with carry bag. Perfect for home workouts.",
            "price": 22.99,
            "image_url": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=400&h=400&fit=crop",
            "category": "Sports",
            "stock": 37,
        },
        {
            "name": "Bluetooth Speaker",
            "description": "Portable waterproof Bluetooth speaker with 360-degree sound and 12-hour battery life.",
            "price": 59.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1677159499898-b061fb5bd2d7?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 19,
        },
        {
            "name": "Cotton Socks Pack",
            "description": "Pack of 10 pairs of comfortable breathable cotton socks in various colours.",
            "price": 12.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1755164641094-3b00ad813362?w=400&h=400&fit=crop",
            "category": "Clothing",
            "stock": 70,
        },
        {
            "name": "Laptop Stand",
            "description": "Ergonomic adjustable laptop stand made of aluminium. Improves posture and desk space.",
            "price": 44.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1683736986821-e4662912a70d?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 21,
        },
        {
            "name": "Meditation Cushion",
            "description": "Round meditation cushion filled with buckwheat. Helps maintain proper posture.",
            "price": 28.99,
            "image_url": "https://images.unsplash.com/photo-1588286840104-8957b019727f?w=400&h=400&fit=crop",
            "category": "Sports",
            "stock": 16,
        },
        {
            "name": "Stainless Steel Lunch Box",
            "description": "Leakproof 3-compartment lunch box made of food-grade stainless steel. Eco-friendly alternative.",
            "price": 31.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1681776287623-c697518f5e5b?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 24,
        },
        {
            "name": "Wireless Charging Pad",
            "description": "10W Qi-certified wireless charging pad with non-slip surface. Compatible with all Qi-enabled devices.",
            "price": 23.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1661481079679-04e8a19e258c?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 39,
        },
        {
            "name": "Lightweight Jacket",
            "description": "Water-resistant lightweight jacket perfect for spring and autumn. Available in multiple colours.",
            "price": 67.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1673356302146-070fd357fe17?w=400&h=400&fit=crop",
            "category": "Clothing",
            "stock": 23,
        },
        {
            "name": "Desk Lamp with Adjustable Arm",
            "description": "Flexible desk lamp with adjustable arm and dimmer control. Energy-efficient LED bulb included.",
            "price": 36.99,
            "image_url": "https://images.unsplash.com/photo-1601642964568-1917224f4e4d?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 17,
        },
        {
            "name": "Multi-Device Charging Station",
            "description": "Organize your cables with this 4-port charging station. Supports fast charging on all ports.",
            "price": 51.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1715115406713-fd67ecea8dcc?w=400&h=400&fit=crop",
            "category": "Electronics",
            "stock": 20,
        },
        {
            "name": "Bamboo Cutting Board",
            "description": "Large bamboo cutting board with juice groove. Naturally antibacterial and sustainable.",
            "price": 21.99,
            "image_url": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 32,
        },
        {
            "name": "Compression Socks",
            "description": "Medical-grade compression socks for improved circulation. Ideal for travel and sports.",
            "price": 19.99,
            "image_url": "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400&h=400&fit=crop",
            "category": "Clothing",
            "stock": 41,
        },
        {
            "name": "Smart Phone Case",
            "description": "Durable protective phone case with shock absorption and raised edges for camera protection.",
            "price": 17.99,
            "image_url": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=400&h=400&fit=crop",
            "category": "Accessories",
            "stock": 58,
        },
        {
            "name": "Exercise Ball",
            "description": "75cm exercise ball with anti-burst design. Perfect for core training and stability work.",
            "price": 25.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1664536968018-47d6812aad88?w=400&h=400&fit=crop",
            "category": "Sports",
            "stock": 14,
        },
        {
            "name": "Minimalist Wallet",
            "description": "Slim design RFID-blocking wallet with multiple card slots. Fits easily in your pocket.",
            "price": 19.49,
            "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop",
            "category": "Accessories",
            "stock": 44,
        },
        {
            "name": "Desk Cable Organizer",
            "description": "Keep cables organized with this sleek cable management system. Flexible and reusable.",
            "price": 11.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1732730224379-8a0805fa27ef?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 52,
        },
    ]

    for data in products_data:
        product = Product(**data)
        session.add(product)
    
    await session.commit()


def get_session():
    """Get async session for use in routes"""
    return async_session()
