import pytest

VALID_USER = {
    "email": "test@example.com",
    "password": "testpassword",
}

async def test_register_user_with_201_with_email_and_password(client):
    response = await client.post("/auth/register", json=VALID_USER)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == VALID_USER["email"]
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()

async def test_register_stores_hashed_password(client, test_db):
    response = await client.post("/auth/register", json=VALID_USER)
    assert response.status_code == 201

    stored_user = await test_db["users"].find_one({"email": VALID_USER["email"]})
    assert stored_user is not None
    assert "hashed_password" in stored_user
    assert stored_user["hashed_password"] != VALID_USER["password"]
    assert stored_user["hashed_password"].startswith("$argon2id$")  # argon2id hash prefix

async def test_register_user_with_existing_email_returns_409_conflict(client):
    response = await client.post("/auth/register", json=VALID_USER)
    assert response.status_code == 201

    response = await client.post("/auth/register", json=VALID_USER)
    assert response.status_code == 409
    data = response.json()["detail"] == "Email already registered"