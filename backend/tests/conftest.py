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
    yield db # run the tests
    # await client.drop_database(settings.MONGO_DB_TEST_NAME) # clean up after tests
