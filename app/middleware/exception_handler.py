from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger

def global_exception_handler(app):
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "An unexpcted internal server error occurred.",
                "detail": str(exc),
                "path": str(request.url.path)
            })