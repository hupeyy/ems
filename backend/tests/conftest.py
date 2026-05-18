import os

os.environ.setdefault("JWT_SECRET_KEY", "dev-secret-key-do-not-use-in-production")  # Use a simple secret key for testing
import httpx
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from app.core.settings import settings
from app.dependencies.employees import get_employee_db
from app.dependencies.users import get_user_db
from app.main import app
from app.db.mongo_db import ensure_indexes


@pytest_asyncio.fixture()
async def client(test_db):
    app.dependency_overrides[get_employee_db] = lambda: test_db
    app.dependency_overrides[get_user_db] = lambda: test_db
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
    

@pytest_asyncio.fixture() # MongoDB connetion fixture
async def test_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.MONGO_DB_TEST_NAME] # use the test database
    for collection in await db.list_collection_names():
        await db.drop_collection(collection) # clear existing data
    await ensure_indexes(db) # ensure indexes are created
    yield db # run the tests
    # await client.drop_database(settings.MONGO_DB_TEST_NAME) # clean up after tests

@pytest_asyncio.fixture()
async def auth_user_client(client):
    user_data = {
        "email": "test@example.com",
        "password": "password12345"
    }

    await client.post("/auth/register", json=user_data)
    response = await client.post("/auth/login", json=user_data)
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client

@pytest_asyncio.fixture()
async def auth_admin_client(client, test_db):
    user_data = {
        "email": "test@example.com",
        "password": "admin123password12345"
    }

    await client.post("/auth/register", json=user_data)
    await test_db.users.update_one({"email": user_data["email"]}, {"$set": {"role": "admin"}})  # Set role to admin

    response = await client.post("/auth/login", json=user_data)
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client
