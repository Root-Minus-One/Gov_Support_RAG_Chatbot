import asyncio
from pymongo import AsyncMongoClient
from loguru import logger

from app.core.config import settings



_client = None

async def init_mongo():
    global _client
    uri = settings.MONGO_DB_URI.get_secret_value()
    _client = AsyncMongoClient(uri)
    await _client.aconnect()
    await _client.admin.command("ping")
    logger.info("successfully connected to MongoDB client")

async def close_mongo():
    global _client
    if _client:
        await _client.close()
        logger.info("MongoDB connection closed")

def get_db():
    global _client
    if _client:
        mongo_db = settings.MONGO_DB_NAME
        _db = _client[mongo_db]
        return _db
    else:
        raise RuntimeError("No database found")

    



# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)