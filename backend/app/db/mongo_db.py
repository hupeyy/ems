from motor.motor_asyncio import AsyncIOMotorClient
from app.core.settings import settings

_client: AsyncIOMotorClient | None = None # connect to the MongoDB server

async def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URL)
    return _client

async def get_db():
    client = await get_client()
    return client[settings.MONGO_DB_NAME]

async def get_test_db():
    client = await get_client()
    return client[settings.MONGO_TEST_DB_NAME]

async def ensure_indexes(db):
    await db.employees.create_index([("employeeId", 1)], unique=True, name="uq_employeeId_index", background=True)

    await db.users.create_index([("email", 1)], unique=True, name="uq_email_index", background=True)



async def close_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None