from app.core.exception_handlers import add_exception_handlers, PreventRedirectMiddleware
from fastapi import FastAPI
from app.api.v1.auth import auth_router
from app.api.v1.leaderboard import leaderboard_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.setting import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Prevent Redirect Middleware
app.add_middleware(PreventRedirectMiddleware)

# Add exception handlers
add_exception_handlers(app)

app.include_router(auth_router.router)
app.include_router(leaderboard_router.router)


# source .venv/bin/activate
# uv add "fastapi[standard]"
# uv run fastapi dev app/main.py --host 192.168.1.106 --port 8000
# for production
# uv sync --frozen --no-cache

# uv add psycopg2-binary
# uv add sqlalchemy
# uv add alembic
# alembic init alembic
# uv run alembic revision --autogenerate -m "Initial migration"
# uv run alembic upgrade head
