import pytest

VALID_USER = {
    "email": "john.doe@example.com",
    "password": "securepassword123"
}

@pytest.fixture
async def auth_token(client):
    await client.post("/auth/register", json=VALID_USER)
    response = await client.post("/auth/login", json=VALID_USER)
    return response.json()["access_token"]

async def test_get_me_with_valid_token_returns_user_info(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/auth/me", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["email"] == VALID_USER["email"]
    assert "password" not in data
    assert "hashed_password" not in data