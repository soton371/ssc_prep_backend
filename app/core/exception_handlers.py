from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from app.core.response import response_failed
from starlette.exceptions import HTTPException as StarletteHTTPException #for handle all exception
from sqlalchemy.exc import IntegrityError


def add_exception_handlers(app):

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return response_failed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message= str(exc) or "An unexpected error occurred. Please try again later.",
        )

        
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return response_failed(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=exc.errors()[0]["msg"],
        )
        

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return response_failed(
            status_code=exc.status_code,
            message=exc.detail,
        )


    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        error_message = str(exc.orig)
        if "duplicate key value violates unique constraint" in error_message:
            platform = error_message.split("=")[1].strip()
            return response_failed(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"{platform}"
            )
        
        return response_failed(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Database integrity error occurred."
        )

