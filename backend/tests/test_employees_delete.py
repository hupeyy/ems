import asyncio

VALID_EMPLOYEE = {
    "employeeId": "EMP00001",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "status": "Active",
    "createdAt": "2024-06-01T12:00:00Z",
}

SECOND_EMPLOYEE = {
    "employeeId": "EMP00002",
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "department": "HR",
    "position": "HR Manager",
    "status": "Active",
    "createdAt": "2024-06-01T12:00:00Z",
}


# ── Happy Path ────────────────────────────────────────────────────────────────

async def test_delete_employee_returns_204(auth_admin_client):
    await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    response = await auth_admin_client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 204


# ── Critical ──────────────────────────────────────────────────────────────────

async def test_delete_employee_removes_document_from_db(auth_admin_client, test_db):
    await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    await auth_admin_client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    stored = await test_db.employees.find_one({"employeeId": VALID_EMPLOYEE["employeeId"]})
    assert stored is None


async def test_delete_employee_makes_get_by_id_return_404(auth_admin_client):
    await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    await auth_admin_client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    response = await auth_admin_client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 404


async def test_delete_employee_removes_only_target_not_others(auth_admin_client):
    await asyncio.gather(
        auth_admin_client.post("/employees", json=VALID_EMPLOYEE),
        auth_admin_client.post("/employees", json=SECOND_EMPLOYEE),
    )
    await auth_admin_client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    response = await auth_admin_client.get(f"/employees/{SECOND_EMPLOYEE['employeeId']}")
    assert response.status_code == 200
    assert response.json()["employeeId"] == SECOND_EMPLOYEE["employeeId"]


async def test_delete_employee_returns_404_for_unknown_id(auth_admin_client):
    response = await auth_admin_client.delete("/employees/UNKNOWN-ID")
    assert response.status_code == 404


async def test_delete_is_idempotent_second_call_returns_404(auth_admin_client):
    await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    await auth_admin_client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    response = await auth_admin_client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 404


# ── Negative ──────────────────────────────────────────────────────────────────

async def test_delete_employee_returns_422_on_malformed_id(auth_admin_client):
    response = await auth_admin_client.delete("/employees/EMP@#$")
    assert response.status_code == 422


async def test_delete_employee_returns_422_on_whitespace_id(auth_admin_client):
    response = await auth_admin_client.delete("/employees/%20")
    assert response.status_code == 422


# ── Edge ─────────────────────────────────────────────────────────────────────

async def test_delete_employee_response_body_is_empty(auth_admin_client):
    await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    response = await auth_admin_client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 204
    assert response.content == b""


async def test_delete_employee_does_not_affect_get_all_count_of_others(auth_admin_client):
    employees = [
        {**VALID_EMPLOYEE, "employeeId": f"EMP{i:05d}", "email": f"emp{i}@example.com"}
        for i in range(1, 4)
    ]
    await asyncio.gather(*[auth_admin_client.post("/employees", json=emp) for emp in employees])

    await auth_admin_client.delete("/employees/EMP00001")

    response = await auth_admin_client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 2
    returned_ids = {e["employeeId"] for e in response.json()}
    assert "EMP001" not in returned_ids
