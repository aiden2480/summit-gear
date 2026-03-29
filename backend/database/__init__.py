import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from database.models import Base, Product

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shop.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
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
            "image_url": "https://images.unsplash.com/photo-1565636192335-14f90427ce45?w=400&h=400&fit=crop",
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
            "image_url": "https://images.unsplash.com/photo-1611996283916-ae2e56feb198?w=400&h=400&fit=crop",
            "category": "Home & Kitchen",
            "stock": 33,
        },
    ]

    for data in products_data:
        product = Product(**data)
        session.add(product)
    
    await session.commit()


def get_session():
    """Get async session for use in routes"""
    return async_session()
