from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.employees import router as employees_router
from app.routes.auth import router as auth_router
from app.core.settings import settings
from app.db.mongo_db import get_db, ensure_indexes, close_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await get_db()
    await ensure_indexes(db)
    yield
    await close_client()

def create_app() -> FastAPI:
    app = FastAPI()
    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(employees_router)
    app.include_router(auth_router)
    return app

app = create_app()