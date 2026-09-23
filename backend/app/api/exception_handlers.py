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
