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
            "name": "Alpine Climbing Helmet",
            "description": "Lightweight ventilated helmet with adjustable fit system. CE/UIAA certified for climbing and mountaineering.",
            "price": 89.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1675461594405-21b579d0aaae?w=400&h=400&fit=crop",
            "category": "Protection",
            "stock": 20,
        },
        {
            "name": "Bouldering Crash Pad",
            "description": "Thick foam crash pad with fold-over design and backpack straps. 100x120cm landing zone.",
            "price": 189.99,
            "image_url": "https://images.unsplash.com/photo-1564769662533-4f00a87b4056?w=400&h=400&fit=crop",
            "category": "Protection",
            "stock": 12,
        },
        {
            "name": "Kids Climbing Helmet",
            "description": "Adjustable youth helmet with fun graphics. Lightweight and comfortable for young climbers.",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1491239300537-f6b9624b283e?w=400&h=400&fit=crop",
            "category": "Protection",
            "stock": 18,
        },
        {
            "name": "Knee Pads (Pair)",
            "description": "Durable neoprene knee pads for crack climbing. Adjustable straps for secure fit.",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1522163182402-834f871fd851?w=400&h=400&fit=crop",
            "category": "Protection",
            "stock": 25,
        },
        {
            "name": "Helmet Headlamp Mount",
            "description": "Universal clip-on headlamp mount compatible with most climbing helmets.",
            "price": 12.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1723809614571-36b11e81672a?w=400&h=400&fit=crop",
            "category": "Protection",
            "stock": 40,
        },
        {
            "name": "Dynamic Climbing Rope 60m",
            "description": "9.8mm single rope with dry treatment. Low impact force and excellent handling.",
            "price": 179.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1661963473217-bbcac070fe34?w=400&h=400&fit=crop",
            "category": "Ropes & Slings",
            "stock": 15,
        },
        {
            "name": "Static Rope 30m",
            "description": "10.5mm static rope for rappelling, hauling, and fixed lines. High abrasion resistance.",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1635360404916-a7919e7de16f?w=400&h=400&fit=crop",
            "category": "Ropes & Slings",
            "stock": 20,
        },
        {
            "name": "Nylon Sling 120cm",
            "description": "Sewn nylon sling rated to 22kN. Versatile for anchors and extensions.",
            "price": 8.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1683850225018-7bd3d7c0317b?w=400&h=400&fit=crop",
            "category": "Ropes & Slings",
            "stock": 60,
        },
        {
            "name": "Dyneema Sling 60cm",
            "description": "Ultra-lightweight Dyneema sling rated to 22kN. 50% lighter than nylon equivalent.",
            "price": 14.99,
            "image_url": "https://images.unsplash.com/photo-1739766191129-1846dda57389?w=400&h=400&fit=crop",
            "category": "Ropes & Slings",
            "stock": 45,
        },
        {
            "name": "Accessory Cord 6mm (per metre)",
            "description": "High-tenacity nylon cord for prusiks and cordelettes. Sold per metre.",
            "price": 1.99,
            "image_url": "https://images.unsplash.com/photo-1557685888-68043f4d680f?w=400&h=400&fit=crop",
            "category": "Ropes & Slings",
            "stock": 200,
        },
        {
            "name": "Rope Bag",
            "description": "Tarp-style rope bag with integrated ground sheet and shoulder straps. Fits up to 80m rope.",
            "price": 39.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1753835628703-027454c0ab90?w=400&h=400&fit=crop",
            "category": "Ropes & Slings",
            "stock": 22,
        },
        {
            "name": "HMS Locking Carabiner",
            "description": "Pear-shaped screwgate carabiner ideal for belaying. 25kN gate-closed strength.",
            "price": 14.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1661604442624-79268aa21f1e?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 50,
        },
        {
            "name": "Wiregate Carabiner (6 Pack)",
            "description": "Lightweight wiregate carabiners for quickdraws and racking. Snag-free nose.",
            "price": 54.99,
            "image_url": "https://images.unsplash.com/photo-1541690090176-17d35a190b6c?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 30,
        },
        {
            "name": "Tubular Belay Device",
            "description": "Classic ATC-style tubular belay and rappel device. Works with ropes 8.5-11mm.",
            "price": 19.99,
            "image_url": "https://images.unsplash.com/photo-1586685256769-4e869a64f1eb?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 35,
        },
        {
            "name": "Assisted Braking Belay Device",
            "description": "Auto-locking belay device with cam-assist braking mechanism. Single rope use.",
            "price": 109.99,
            "image_url": "https://images.unsplash.com/photo-1699854427517-1356983b38e7?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 18,
        },
        {
            "name": "Figure 8 Descender",
            "description": "Classic figure-8 rappel device machined from aircraft aluminium. 40kN rated.",
            "price": 16.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1683850225155-0d22264379c0?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 28,
        },
        {
            "name": "Quickdraw Set (6 Pack)",
            "description": "Pre-built sport climbing quickdraws with wiregate carabiners and Dyneema dogbone.",
            "price": 69.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1753835666350-7e07f6b22f87?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 25,
        },
        {
            "name": "Rescue Pulley",
            "description": "Single sheave pulley for hauling systems and crevasse rescue. Fits ropes up to 13mm.",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1774534576776-b350742e3dc8?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 20,
        },
        {
            "name": "Nut Set (Stoppers)",
            "description": "Set of 10 wired stoppers for traditional climbing protection. Colour-coded by size.",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1662572995219-4d68a9fc8640?w=400&h=400&fit=crop",
            "category": "Hardware",
            "stock": 16,
        },
        {
            "name": "All-Round Climbing Harness",
            "description": "Versatile 4-season harness with adjustable leg loops. Suitable for sport, trad, and ice climbing.",
            "price": 69.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1675461588319-1f6f0a41ff15?w=400&h=400&fit=crop",
            "category": "Harnesses",
            "stock": 22,
        },
        {
            "name": "Lightweight Sport Harness",
            "description": "Minimalist harness for gym and sport climbing. Breathable mesh construction.",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1677918903267-c213ce2c1ff8?w=400&h=400&fit=crop",
            "category": "Harnesses",
            "stock": 30,
        },
        {
            "name": "Alpine Harness",
            "description": "Ultra-light mountaineering harness with removable leg loops. Fits over crampons and ski boots.",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1765064520254-229dbf995bcb?w=400&h=400&fit=crop",
            "category": "Harnesses",
            "stock": 14,
        },
        {
            "name": "Chest Harness",
            "description": "Supplementary chest harness for via ferrata and caving. Keeps torso upright during falls.",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1764925925846-f4bd8e3c1703?w=400&h=400&fit=crop",
            "category": "Harnesses",
            "stock": 16,
        },
        {
            "name": "Aggressive Climbing Shoes",
            "description": "Downturned bouldering shoes with sticky rubber sole. Precise edging and toe hooking.",
            "price": 149.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1672280913342-06cfe011bc62?w=400&h=400&fit=crop",
            "category": "Footwear",
            "stock": 18,
        },
        {
            "name": "All-Round Climbing Shoes",
            "description": "Flat-lasted multipurpose shoes comfortable for long routes. Great for beginners and all-day wear.",
            "price": 99.99,
            "image_url": "https://images.unsplash.com/photo-1685514371031-b30c30b5b232?w=400&h=400&fit=crop",
            "category": "Footwear",
            "stock": 25,
        },
        {
            "name": "Crack Climbing Shoes",
            "description": "Flat stiff shoes designed for jamming. High-top ankle protection with lace closure.",
            "price": 129.99,
            "image_url": "https://images.unsplash.com/photo-1606166187734-a4cb74079037?w=400&h=400&fit=crop",
            "category": "Footwear",
            "stock": 14,
        },
        {
            "name": "Approach Shoes",
            "description": "Sticky rubber hiking shoes with climbing-zone toe. Perfect for the walk to the crag.",
            "price": 119.99,
            "image_url": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=400&fit=crop",
            "category": "Footwear",
            "stock": 20,
        },
        {
            "name": "Climbing Shoe Resole Kit",
            "description": "DIY resole kit with 4mm Vibram rubber sheet, contact cement, and sandpaper.",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&h=400&fit=crop",
            "category": "Footwear",
            "stock": 30,
        },
        {
            "name": "Chalk Bag",
            "description": "Drawstring chalk bag with fleece lining and belt loop. Holds 200g of chalk.",
            "price": 19.99,
            "image_url": "https://images.unsplash.com/photo-1596548574786-dc8790fe0683?w=400&h=400&fit=crop",
            "category": "Apparel",
            "stock": 40,
        },
        {
            "name": "Chalk Ball (Refill)",
            "description": "Mesh chalk ball with 65g of high-friction magnesium carbonate. Less mess than loose chalk.",
            "price": 5.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1675461585652-2fcdb84e43b0?w=400&h=400&fit=crop",
            "category": "Apparel",
            "stock": 80,
        },
        {
            "name": "Climbing Pants",
            "description": "Stretchy and durable softshell pants with gusseted crotch. Articulated knees for freedom of movement.",
            "price": 79.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1753835628730-26bb31823a51?w=400&h=400&fit=crop",
            "category": "Apparel",
            "stock": 22,
        },
        {
            "name": "Belay Gloves",
            "description": "Full-grain leather gloves for belaying and rappelling. Reinforced palm for heat resistance.",
            "price": 29.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1672281090478-9b3ad329ad88?w=400&h=400&fit=crop",
            "category": "Apparel",
            "stock": 28,
        },
        {
            "name": "Climbing Beanie",
            "description": "Merino wool beanie perfect for cold belays. Moisture-wicking and odour resistant.",
            "price": 24.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1672883552656-be33f579fc4b?w=400&h=400&fit=crop",
            "category": "Apparel",
            "stock": 35,
        },
        {
            "name": "Finger Tape (5 Pack)",
            "description": "1.5cm wide cotton climbing tape for finger support. Pack of 5 rolls in assorted colours.",
            "price": 9.99,
            "image_url": "https://plus.unsplash.com/premium_photo-1712438458571-a5b5cb9d98a6?w=400&h=400&fit=crop",
            "category": "Apparel",
            "stock": 55,
        },
    ]

    for data in products_data:
        product = Product(**data)
        session.add(product)
    
    await session.commit()


def get_session():
    """Get async session for use in routes"""
    return async_session()
