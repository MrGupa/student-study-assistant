import logging

from fastapi import FastAPI

from app.core.logging import configure_logging

app = FastAPI()

configure_logging()

logger = logging.getLogger(__name__)

logger.info("Starting Student Study Assistant backend.")

