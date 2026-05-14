import pytest
import app.core.settings as settings
from app.db.mongo_db import get_client
from unittest.mock import MagicMock, AsyncMock


@pytest.mark.asyncio
async def test_mongo_connection_ok(test_db):    # driving test case
    # Test if we can connect to the test database and perform a simple operation
    assert test_db is not None
    assert test_db.name == settings.settings.MONGO_DB_TEST_NAME


@pytest.mark.asyncio
async def test_mongo_connection_testdb_ping(test_db):  # driving test case
    ping_result = await test_db.command("ping")
    assert ping_result.get("ok") == 1.0

##
# @pytest.mark.asyncio
# async def test_mongo_connection_ping(): # characterization test case -- code was already written; expected to pass
#     client = await get_client()
#     ping_result = await client.admin.command("ping")
#     assert ping_result.get("ok") == 1.0


# To test document insertion and retrieval
@pytest.mark.asyncio
async def test_mongo_connection_testdb_insert_and_find(test_db): # characterization test case -- code was already written; expected to pass
    # insert a test document
    test_doc = {"name": "Test Document", "value": 42}
    insert_result = await test_db.test_collection.insert_one(test_doc)
    assert insert_result.inserted_id is not None

    # retrieve the inserted document
    found_doc = await test_db.test_collection.find_one({"_id": insert_result.inserted_id})
    assert found_doc is not None
    assert found_doc["name"] == test_doc["name"]
    assert found_doc["value"] == test_doc["value"]


# Using mock

@pytest.mark.asyncio
async def test_mongo_connection_testdb_mock_ping(test_db): # characterization test case -- code was already written; expected to pass
    fake_client = MagicMock() # Create a mock client
    
    # Mock the admin.command method to return a successful ping response
    fake_client.admin.command = AsyncMock(return_value={"ok": 1.0})
    result = await fake_client.admin.command("ping") # Call the mocked ping command

    assert result.get("ok") == 1.0 # Assert that the mocked response is as expected