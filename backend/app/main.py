import logging

from fastapi import FastAPI

from app.api.exception_handlers import (
    account_inactive_handler,
    email_already_exists_handler,
    invalid_credentials_handler,
    user_not_found_handler,
)
from app.api.router import api_router
from app.common.exceptions import (
    AccountInactiveError,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.common.exceptions.user import UserNotFoundError
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
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(EmailAlreadyRegisteredError, email_already_exists_handler)
app.add_exception_handler(InvalidCredentialsError,invalid_credentials_handler)
app.add_exception_handler(AccountInactiveError,account_inactive_handler)
