import aiosqlite
import json
import os

BACKEND_DIR = os.path.dirname(__file__)
SEED_PATH = os.path.join(BACKEND_DIR, "seed.sql")
DB_PATH = os.path.join(BACKEND_DIR, "shop.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        with open(SEED_PATH) as fp:
            await db.executescript(fp.read())
            await db.commit()

def get_db():
    return aiosqlite.connect(DB_PATH)
