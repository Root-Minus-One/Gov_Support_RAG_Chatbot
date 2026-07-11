# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger


from app.core.logger import setup_logging
from app.db.db_conn import init_pool, close_pool
from app.core.config import settings
### Main.py is the app and the routes are in routes.py and when api call happens it goes to routes.py from 


setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await init_pool()
    yield
    await close_pool()

app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    logger.info("Health check called")
    return {"status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION}