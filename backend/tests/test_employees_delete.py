import asyncio

VALID_EMPLOYEE = {
    "employeeId": "EMP001",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "status": "Active",
    "createdAt": "2024-06-01T12:00:00Z",
}

SECOND_EMPLOYEE = {
    "employeeId": "EMP002",
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "department": "HR",
    "position": "HR Manager",
    "status": "Active",
    "createdAt": "2024-06-01T12:00:00Z",
}


# ── Happy Path ────────────────────────────────────────────────────────────────

async def test_delete_employee_returns_204(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 204


# ── Critical ──────────────────────────────────────────────────────────────────

async def test_delete_employee_removes_document_from_db(client, test_db):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    stored = await test_db.employees.find_one({"employeeId": VALID_EMPLOYEE["employeeId"]})
    assert stored is None


async def test_delete_employee_makes_get_by_id_return_404(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    response = await client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 404


async def test_delete_employee_removes_only_target_not_others(client):
    await asyncio.gather(
        client.post("/employees", json=VALID_EMPLOYEE),
        client.post("/employees", json=SECOND_EMPLOYEE),
    )
    await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    response = await client.get(f"/employees/{SECOND_EMPLOYEE['employeeId']}")
    assert response.status_code == 200
    assert response.json()["employeeId"] == SECOND_EMPLOYEE["employeeId"]


async def test_delete_employee_returns_404_for_unknown_id(client):
    response = await client.delete("/employees/UNKNOWN-ID")
    assert response.status_code == 404


async def test_delete_is_idempotent_second_call_returns_404(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    response = await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 404


# ── Negative ──────────────────────────────────────────────────────────────────

async def test_delete_employee_returns_422_on_malformed_id(client):
    response = await client.delete("/employees/EMP@#$")
    assert response.status_code == 422


async def test_delete_employee_returns_422_on_whitespace_id(client):
    response = await client.delete("/employees/%20")
    assert response.status_code == 422


# ── Edge ─────────────────────────────────────────────────────────────────────

async def test_delete_employee_response_body_is_empty(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 204
    assert response.content == b""


async def test_delete_employee_does_not_affect_get_all_count_of_others(client):
    employees = [
        {**VALID_EMPLOYEE, "employeeId": f"EMP{i:03d}", "email": f"emp{i}@example.com"}
        for i in range(1, 4)
    ]
    await asyncio.gather(*[client.post("/employees", json=emp) for emp in employees])

    await client.delete("/employees/EMP001")

    response = await client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 2
    returned_ids = {e["employeeId"] for e in response.json()}
    assert "EMP001" not in returned_ids
