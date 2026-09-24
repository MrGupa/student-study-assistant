from fastapi import Request
from fastapi.responses import JSONResponse


async def user_not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"},
    )


async def email_already_exists_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=409,
        content={"detail": "Email already exists"},
    )


async def invalid_credentials_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid email or password"},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def account_inactive_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=403,
        content={"detail": "Inactive account"},
    )
