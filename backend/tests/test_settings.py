import pytest

def test_settings_load_defaults_when_env_missing():
    from app.core.settings import Settings
    settings = Settings()
    assert settings.APP_ENV == "development"
    assert settings.APP_NAME == "EMS"
    assert settings.MONGO_URL == "mongodb://localhost:27017"
    assert settings.MONGO_DB_NAME == "ems_db"
    assert settings.MONGO_DB_TEST_NAME== "ems_test_db"

def test_settings_read_mongo_uri_from_env(monkeypatch):
    from app.core.settings import Settings
    test_uri = "mongodb://testhost:27017"
    monkeypatch.setenv("MONGO_URL", test_uri)
    settings = Settings()
    assert settings.MONGO_URL == test_uri