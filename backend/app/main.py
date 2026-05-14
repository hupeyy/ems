from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.employees import router as employees_router
from app.core.settings import settings

def create_app() -> FastAPI:
    app = FastAPI()
    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(employees_router)
    return app

app = create_app()