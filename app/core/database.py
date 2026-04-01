import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "recruitment_db")

class Database:
    client: AsyncIOMotorClient = None

db_obj = Database()

async def get_db():
    if db_obj.client is None:
        raise Exception("Database not initialized")
    return db_obj.client[MONGODB_DB_NAME]
