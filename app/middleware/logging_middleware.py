from loguru import logger
import time

def setup_logging_middleware(app):
    @app.middleware("http")
    async def log_middleware(request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        logger.info(f"'method': {request.method}, 'path': {request.url.path}, 'status': {response.status_code}, 'duration': {duration}")
        return response