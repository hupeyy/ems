import pytest
from app.core.settings import settings

def test_create_app_returns_fastapi_instance():
    from app.main import create_app
    app = create_app()
    assert app is not None
    assert hasattr(app, "router")

def test_app_includes_health_route():
    from app.main import create_app
    app = create_app()
    routes = [route.path for route in app.routes]
    assert "/health" in routes

def test_app_loads_settings_into_state():
    from app.main import create_app
    app = create_app()
    assert hasattr(app.state, "settings")
    assert app.state.settings is not None
    assert app.state.settings.MONGO_URL == settings.MONGO_URL
