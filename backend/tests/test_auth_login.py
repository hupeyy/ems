import pytest

VALID_USER = {
    "email": "john.doe@example.com",
    "password": "securepassword123"
}

@pytest.fixture
async def registered_user(client):
    response = await client.post("/auth/register", json=VALID_USER)
    assert response.status_code == 201
    return VALID_USER

async def test_login_user_with_valid_credentials(client, registered_user):
    response = await client.post("/auth/login", json=registered_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"