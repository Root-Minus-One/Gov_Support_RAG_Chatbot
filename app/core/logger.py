from loguru import logger
import sys

from app.core.config import settings

def setup_logging():
    logger.remove()
    set_log_level = settings.LOG_LEVEL.upper()

    if settings.ENVIRONMENT == "development":
        dev_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
        logger.add(sys.stdout, serialize=False, format=dev_format, level=set_log_level
        )
    elif settings.ENVIRONMENT in ("production", "staging"):
        logger.add(
            "logs/app.log",
            serialize=True,
            level=set_log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )