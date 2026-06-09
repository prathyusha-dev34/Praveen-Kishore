from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi.exceptions import (
    RequestValidationError
)

from starlette.status import (
    HTTP_400_BAD_REQUEST
)


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": "Invalid request"
        }
    )