import os
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from database.models import Product, CartItem

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shop.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db(*_):
    """Initialize database and seed with data"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

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
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLA042VA.jpg?20240208113436",
            "category": "Protection",
            "stock": 20,
        },
        {
            "name": "Bouldering Crash Pad",
            "description": "Thick foam crash pad with fold-over design and backpack straps. 100x120cm landing zone.",
            "price": 189.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLCIRRO.jpg?20221202154635",
            "category": "Protection",
            "stock": 12,
        },
        {
            "name": "Kids Climbing Helmet",
            "description": "Adjustable youth helmet with fun graphics. Lightweight and comfortable for young climbers.",
            "price": 49.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/FIXE872G.jpg?20221202154635",
            "category": "Protection",
            "stock": 18,
        },
        {
            "name": "Knee Pads (Pair)",
            "description": "Durable neoprene knee pads for crack climbing. Adjustable straps for secure fit.",
            "price": 34.99,
            "image_url": "https://www.e9planet.com/cdn/shop/files/09-FW233496_1200x630.jpg?v=1697725799",
            "category": "Protection",
            "stock": 25,
        },
        {
            "name": "Helmet Headlamp Mount",
            "description": "Universal clip-on headlamp mount compatible with most climbing helmets.",
            "price": 12.99,
            "image_url": "https://brightguy.com/wp-content/uploads/Petzl-UNI-Adapt-Headlamp-Adhesive-Clips.jpg",
            "category": "Protection",
            "stock": 40,
        },
        {
            "name": "Dynamic Climbing Rope 60m",
            "description": "9.8mm single rope with dry treatment. Low impact force and excellent handling.",
            "price": 179.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLCONTACT.webp?20250324083929",
            "category": "Ropes & Slings",
            "stock": 15,
        },
        {
            "name": "Static Rope 30m",
            "description": "10.5mm static rope for rappelling, hauling, and fixed lines. High abrasion resistance.",
            "price": 89.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/EDL8325.webp?20250703111348",
            "category": "Ropes & Slings",
            "stock": 20,
        },
        {
            "name": "Nylon Sling 120cm",
            "description": "Sewn nylon sling rated to 22kN. Versatile for anchors and extensions.",
            "price": 8.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/WC10036.webp?20250130123447",
            "category": "Ropes & Slings",
            "stock": 60,
        },
        {
            "name": "Dyneema Sling 60cm",
            "description": "Ultra-lightweight Dyneema sling rated to 22kN. 50% lighter than nylon equivalent.",
            "price": 14.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/WCDS10.webp?20241114112520",
            "category": "Ropes & Slings",
            "stock": 45,
        },
        {
            "name": "Accessory Cord 6mm (per metre)",
            "description": "High-tenacity nylon cord for prusiks and cordelettes. Sold per metre.",
            "price": 1.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/TR6.jpg?20221202154635",
            "category": "Ropes & Slings",
            "stock": 200,
        },
        {
            "name": "Rope Bag",
            "description": "Tarp-style rope bag with integrated ground sheet and shoulder straps. Fits up to 80m rope.",
            "price": 39.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/8BROPEBAG.jpg?20231218142013",
            "category": "Ropes & Slings",
            "stock": 22,
        },
        {
            "name": "HMS Locking Carabiner",
            "description": "Pear-shaped screwgate carabiner ideal for belaying. 25kN gate-closed strength.",
            "price": 14.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/WC1001.webp?20250328104526",
            "category": "Hardware",
            "stock": 50,
        },
        {
            "name": "Wiregate Carabiner (6 Pack)",
            "description": "Lightweight wiregate carabiners for quickdraws and racking. Snag-free nose.",
            "price": 54.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/BDLITEWIRE.webp?20250328105628",
            "category": "Hardware",
            "stock": 30,
        },
        {
            "name": "Tubular Belay Device",
            "description": "Classic ATC-style tubular belay and rappel device. Works with ropes 8.5-11mm.",
            "price": 19.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/BDATCXPS16.webp?20251204151429",
            "category": "Hardware",
            "stock": 35,
        },
        {
            "name": "Assisted Braking Belay Device",
            "description": "Auto-locking belay device with cam-assist braking mechanism. Single rope use.",
            "price": 109.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLGRIGRI.webp?20250611111019",
            "category": "Hardware",
            "stock": 18,
        },
        {
            "name": "Figure 8 Descender",
            "description": "Classic figure-8 rappel device machined from aircraft aluminium. 40kN rated.",
            "price": 16.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/CAMP092801.jpg?20221202154635",
            "category": "Hardware",
            "stock": 28,
        },
        {
            "name": "Quickdraw Set (6 Pack)",
            "description": "Pre-built sport climbing quickdraws with wiregate carabiners and Dyneema dogbone.",
            "price": 69.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLM060LC05.jpg?20231002151316",
            "category": "Hardware",
            "stock": 25,
        },
        {
            "name": "Rescue Pulley",
            "description": "Single sheave pulley for hauling systems and crevasse rescue. Fits ropes up to 13mm.",
            "price": 29.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLRESCUEPUL.jpg?20221202154635",
            "category": "Hardware",
            "stock": 20,
        },
        {
            "name": "Nut Set (Stoppers)",
            "description": "Set of 10 wired stoppers for traditional climbing protection. Colour-coded by size.",
            "price": 49.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/BDSTOPPER413.jpg?20221202154635",
            "category": "Hardware",
            "stock": 16,
        },
        {
            "name": "All-Round Climbing Harness",
            "description": "Versatile 4-season harness with adjustable leg loops. Suitable for sport, trad, and ice climbing.",
            "price": 69.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLH635C052A.jpg?20240409123439",
            "category": "Harnesses",
            "stock": 22,
        },
        {
            "name": "Lightweight Sport Harness",
            "description": "Minimalist harness for gym and sport climbing. Breathable mesh construction.",
            "price": 49.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLSELENA21.jpg?20221202154635",
            "category": "Harnesses",
            "stock": 30,
        },
        {
            "name": "Alpine Harness",
            "description": "Ultra-light mountaineering harness with removable leg loops. Fits over crampons and ski boots.",
            "price": 89.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/CAMP205.jpg?20221202154635",
            "category": "Harnesses",
            "stock": 14,
        },
        {
            "name": "Chest Harness",
            "description": "Supplementary chest harness for via ferrata and caving. Keeps torso upright during falls.",
            "price": 34.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLVOLT.jpg?20221202154635",
            "category": "Harnesses",
            "stock": 16,
        },
        {
            "name": "Aggressive Climbing Shoes",
            "description": "Downturned bouldering shoes with sticky rubber sole. Precise edging and toe hooking.",
            "price": 149.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/SCARPADRAGO.webp?20260106142341",
            "category": "Footwear",
            "stock": 18,
        },
        {
            "name": "All-Round Climbing Shoes",
            "description": "Flat-lasted multipurpose shoes comfortable for long routes. Great for beginners and all-day wear.",
            "price": 99.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/SCARPAVELOCE.webp?20250527124904",
            "category": "Footwear",
            "stock": 25,
        },
        {
            "name": "Crack Climbing Shoes",
            "description": "Flat stiff shoes designed for jamming. High-top ankle protection with lace closure.",
            "price": 129.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/BUTORAACROCOMP.webp?20250527140334",
            "category": "Footwear",
            "stock": 14,
        },
        {
            "name": "Approach Shoes",
            "description": "Sticky rubber hiking shoes with climbing-zone toe. Perfect for the walk to the crag.",
            "price": 119.99,
            "image_url": "https://k2.com.au/cdn/shop/collections/Approach-283710.jpg?v=1663235186",
            "category": "Footwear",
            "stock": 20,
        },
        {
            "name": "Climbing Shoe Resole Kit",
            "description": "DIY resole kit with 4mm Vibram rubber sheet, contact cement, and sandpaper.",
            "price": 29.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/PETZLH750A073.jpg?20240618115158",
            "category": "Footwear",
            "stock": 30,
        },
        {
            "name": "Chalk Bag",
            "description": "Drawstring chalk bag with fleece lining and belt loop. Holds 200g of chalk.",
            "price": 19.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/8BPLUSCB-01.webp?20250815140519",
            "category": "Apparel",
            "stock": 40,
        },
        {
            "name": "Chalk Ball (Refill)",
            "description": "Mesh chalk ball with 65g of high-friction magnesium carbonate. Less mess than loose chalk.",
            "price": 5.99,
            "image_url": "https://szent.com.au/cdn/shop/products/Xchalk_ball1.jpg?v=1544370816",
            "category": "Apparel",
            "stock": 80,
        },
        {
            "name": "Climbing Pants",
            "description": "Stretchy and durable softshell pants with gusseted crotch. Articulated knees for freedom of movement.",
            "price": 79.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/E9S25UTR004.webp?20251104144423",
            "category": "Apparel",
            "stock": 22,
        },
        {
            "name": "Belay Gloves",
            "description": "Full-grain leather gloves for belaying and rappelling. Reinforced palm for heat resistance.",
            "price": 29.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/MT-BELAY.jpg?20221202154635",
            "category": "Apparel",
            "stock": 28,
        },
        {
            "name": "Climbing Beanie",
            "description": "Merino wool beanie perfect for cold belays. Moisture-wicking and odour resistant.",
            "price": 24.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/CA-004.jpg?20240122151653",
            "category": "Apparel",
            "stock": 35,
        },
        {
            "name": "Finger Tape (5 Pack)",
            "description": "1.5cm wide cotton climbing tape for finger support. Pack of 5 rolls in assorted colours.",
            "price": 9.99,
            "image_url": "https://www.climbinganchors.com.au/assets/full/8B80300.jpg?20240905135651",
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
