import aiosqlite
import json
import os

BACKEND_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BACKEND_DIR)
DB_PATH = os.path.join(BACKEND_DIR, "shop.db")
SEED_PATH = os.path.join(PROJECT_DIR, "seed_data.json")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                image_url TEXT NOT NULL,
                category TEXT NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)
        await db.commit()

        cursor = await db.execute("SELECT COUNT(*) FROM products")
        row = await cursor.fetchone()
        if row[0] == 0:
            await seed_db(db)


async def seed_db(db):
    if not os.path.exists(SEED_PATH):
        return
    with open(SEED_PATH, "r") as f:
        products = json.load(f)
    for p in products:
        await db.execute(
            "INSERT INTO products (name, description, price, image_url, category, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (p["name"], p["description"], p["price"], p["image_url"], p["category"], p["stock"]),
        )
    await db.commit()


def get_db():
    return aiosqlite.connect(DB_PATH)
