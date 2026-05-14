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