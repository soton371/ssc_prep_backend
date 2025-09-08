from typing import Union

from fastapi import FastAPI
from app.api.v1.auth import auth_router
from app.api.v1.leaderboard import leaderboard_router

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(leaderboard_router.router)



# source .venv/bin/activate
# uv add "fastapi[standard]"
# uv run fastapi dev app/main.py --host 192.168.1.109 --port 8000
# for production
# uv sync --frozen --no-cache

# uv add psycopg2-binary
# uv add sqlalchemy
# uv add alembic
# alembic init alembic
# uv run alembic revision --autogenerate -m "Initial migration"
# uv run alembic upgrade head