from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from app.core.response import response_failed
# for handle all exception
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware



def add_exception_handlers(app):
    # for handle google token error
    @app.exception_handler(ValueError)
    async def google_exception_handler(request: Request, exc: Exception):
        return response_failed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Invalid credentials or token error.",
        )

    # for handle all uncaught exception
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return response_failed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(
                exc) or "An unexpected error occurred. Please try again later.",
        )

    # for handle pydantic validation error
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return response_failed(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=exc.errors()[0]["msg"],
        )

        # for handle http exception
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return response_failed(
            status_code=exc.status_code,
            message=exc.detail,
        )

    # for handle database integrity error
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


# Custom middleware to prevent 307 Temporary Redirect
class PreventRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if path mismatch হচ্ছে (trailing slash issue)
        if request.url.path.endswith("/") and not any(
            route.path == request.url.path for route in request.app.router.routes
        ):
            return response_failed(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Not Found. Remove the trailing slash.",
            )

        if not request.url.path.endswith("/") and any(
            route.path == request.url.path + "/" for route in request.app.router.routes
        ):
            return response_failed(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Not Found. Add a trailing slash.",
            )
        return await call_next(request)
