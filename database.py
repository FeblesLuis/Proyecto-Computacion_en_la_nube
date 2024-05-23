import os
from motor.motor_asyncio import AsyncIOMotorClient

async def get_database():
    mongodb_client = AsyncIOMotorClient(os.environ.get("MONGODB_URI"))
    mongodb = mongodb_client["mydatabase"]
    yield mongodb
    mongodb_client.close()
