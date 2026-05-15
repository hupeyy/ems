VALID_EMPLOYEE = {
    "employeeId": "EMP001",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "status": "Active",
    "updatedAt": "2024-06-01T12:00:00Z",
}


# ── Happy Path ────────────────────────────────────────────────────────────────

async def test_put_employee_returns_200_with_updated_field(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


async def test_put_employee_can_update_single_field(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"department": "Marketing"})
    assert response.status_code == 200
    assert response.json()["department"] == "Marketing"


async def test_put_employee_can_update_all_fields_at_once(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    updates = {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "department": "HR",
        "position": "HR Manager",
        "status": "Inactive",
    }
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json=updates)
    assert response.status_code == 200
    data = response.json()
    for field, value in updates.items():
        assert data[field] == value


# ── Critical ──────────────────────────────────────────────────────────────────

async def test_put_employee_persists_changes_to_db(client, test_db):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "Persisted Name"})
    stored = await test_db.employees.find_one({"employeeId": VALID_EMPLOYEE["employeeId"]})
    assert stored["name"] == "Persisted Name"


async def test_put_employee_does_not_overwrite_unchanged_fields(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "New Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == VALID_EMPLOYEE["email"]
    assert data["department"] == VALID_EMPLOYEE["department"]
    assert data["position"] == VALID_EMPLOYEE["position"]
    assert data["status"] == VALID_EMPLOYEE["status"]


async def test_put_employee_returns_404_for_unknown_id(client):
    response = await client.put("/employees/UNKNOWN-ID", json={"name": "New Name"})
    assert response.status_code == 404


async def test_put_employee_updatedAt_is_set_automatically(client, test_db):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "Updated Name"})
    stored = await test_db.employees.find_one({"employeeId": VALID_EMPLOYEE["employeeId"]})
    assert stored.get("updatedAt") is not None


# ── Negative ──────────────────────────────────────────────────────────────────

async def test_put_employee_returns_422_on_empty_body(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={})
    assert response.status_code == 422


async def test_put_employee_returns_422_on_invalid_email(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"email": "not-an-email"})
    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]


async def test_put_employee_returns_422_on_name_too_short(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": ""})
    assert response.status_code == 422
    assert "name" in response.json()["detail"][0]["loc"]


async def test_put_employee_returns_422_on_malformed_id(client):
    response = await client.put("/employees/EMP@#$", json={"name": "New Name"})
    assert response.status_code == 422


async def test_put_employee_cannot_update_employeeId(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(
        f"/employees/{VALID_EMPLOYEE['employeeId']}",
        json={"employeeId": "DIFFERENT-ID", "name": "New Name"},
    )
    assert response.status_code == 200
    assert response.json()["employeeId"] == VALID_EMPLOYEE["employeeId"]


# ── Edge ─────────────────────────────────────────────────────────────────────

async def test_put_employee_with_same_value_returns_200_no_error(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(
        f"/employees/{VALID_EMPLOYEE['employeeId']}",
        json={"name": VALID_EMPLOYEE["name"]},
    )
    assert response.status_code == 200
    assert response.json()["name"] == VALID_EMPLOYEE["name"]


async def test_put_employee_with_extra_unknown_fields_ignored(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.put(
        f"/employees/{VALID_EMPLOYEE['employeeId']}",
        json={"name": "New Name", "unknownField": "should be ignored"},
    )
    assert response.status_code == 200
    assert "unknownField" not in response.json()
    assert response.json()["name"] == "New Name"


async def test_put_employee_sequential_updates_reflect_latest_state(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "First Update"})
    response = await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "Second Update"})
    assert response.status_code == 200
    assert response.json()["name"] == "Second Update"
