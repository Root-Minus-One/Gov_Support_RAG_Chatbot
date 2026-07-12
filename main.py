### Main.py is the app and the routes are in routes.py and when api call happens it goes to routes.py 

from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger


from app.core.logger import setup_logging
from app.db.postgres import init_pool, close_pool
from app.db.mongo import init_mongo, close_mongo, get_db
from app.core.config import settings



@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    try:
        await init_pool()
    except Exception as e:
        logger.error(f"Postgres connection failed {e}")
        raise
    try:
        await init_mongo()
    except Exception as e:
        logger.error(f"Mongo connection failed {e}")
        raise

    try:
        yield
    finally:
        await close_pool()
        await close_mongo()
    
app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    logger.info("Health check called")
    return {"status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION}