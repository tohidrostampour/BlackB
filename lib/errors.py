from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    pass


def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )
