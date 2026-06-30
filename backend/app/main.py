import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

logger.info("Starting Student Study Assistant backend.")

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(api_router)
