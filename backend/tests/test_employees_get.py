import asyncio
import pytest

VALID_EMPLOYEE = {
    "employeeId": "EMP001",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "status": "Active",
    "createdAt": "2024-06-01T12:00:00Z",
}

EXPECTED_FIELDS = {"employeeId", "name", "email", "department", "position", "status", "createdAt"}


# ── Happy Path ────────────────────────────────────────────────────────────────

async def test_get_all_employees_returns_200_with_empty_list(client):
    response = await client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_all_employees_returns_one_after_post(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_employees_returns_correct_fields_on_each_item(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.get("/employees")
    assert response.status_code == 200
    assert EXPECTED_FIELDS == set(response.json()[0].keys())


# ── Critical ──────────────────────────────────────────────────────────────────

async def test_get_all_employees_returns_multiple_after_multiple_posts(client):
    employees = [
        {**VALID_EMPLOYEE, "employeeId": f"EMP{i:03d}", "email": f"emp{i}@example.com"}
        for i in range(1, 4)
    ]
    await asyncio.gather(*[client.post("/employees", json=emp) for emp in employees])

    response = await client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_all_employees_does_not_return_deleted_employee(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")

    response = await client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_all_employees_reflects_updated_fields_after_put(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "Jane Doe"})

    response = await client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"


# ── Negative ──────────────────────────────────────────────────────────────────

async def test_get_all_employees_returns_list_not_dict(client):
    response = await client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_all_employees_does_not_expose_mongo_underscore_id(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.get("/employees")
    assert response.status_code == 200
    for item in response.json():
        assert "_id" not in item


# ── Edge ─────────────────────────────────────────────────────────────────────

async def test_get_all_employees_with_100_records_returns_all(client, test_db):
    from datetime import datetime, timezone

    docs = [
        {
            "employeeId": f"EMP{i:03d}",
            "name": f"Employee {i}",
            "email": f"emp{i}@example.com",
            "department": "Engineering",
            "position": "Engineer",
            "status": "Active",
            "createdAt": datetime.now(timezone.utc),
        }
        for i in range(1, 101)
    ]
    await test_db.employees.insert_many(docs)

    response = await client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 100


async def test_get_all_employees_returns_200_not_404_when_empty(client):
    response = await client.get("/employees")
    assert response.status_code == 200


# ── GET /employees/{id} ───────────────────────────────────────────────────────

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

async def test_get_employee_by_id_returns_200_with_correct_shape(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 200
    assert EXPECTED_FIELDS == set(response.json().keys())


async def test_get_employee_by_id_returns_all_fields(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    response = await client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 200
    data = response.json()
    assert data["employeeId"] == VALID_EMPLOYEE["employeeId"]
    assert data["name"] == VALID_EMPLOYEE["name"]
    assert data["email"] == VALID_EMPLOYEE["email"]
    assert data["department"] == VALID_EMPLOYEE["department"]
    assert data["position"] == VALID_EMPLOYEE["position"]
    assert data["status"] == VALID_EMPLOYEE["status"]


async def test_get_employee_by_id_returns_correct_employee_not_another(client):
    await asyncio.gather(
        client.post("/employees", json=VALID_EMPLOYEE),
        client.post("/employees", json=SECOND_EMPLOYEE),
    )
    response = await client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 200
    assert response.json()["employeeId"] == VALID_EMPLOYEE["employeeId"]
    assert response.json()["name"] == VALID_EMPLOYEE["name"]


# ── Critical ──────────────────────────────────────────────────────────────────

async def test_get_employee_by_id_returns_404_for_unknown_id(client):
    response = await client.get("/employees/UNKNOWN-ID")
    assert response.status_code == 404


async def test_get_employee_by_id_returns_updated_data_after_put(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.put(f"/employees/{VALID_EMPLOYEE['employeeId']}", json={"name": "Updated Name"})
    response = await client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


async def test_get_employee_by_id_returns_404_after_delete(client):
    await client.post("/employees", json=VALID_EMPLOYEE)
    await client.delete(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    response = await client.get(f"/employees/{VALID_EMPLOYEE['employeeId']}")
    assert response.status_code == 404


# ── Negative ──────────────────────────────────────────────────────────────────

async def test_get_employee_by_id_returns_422_on_malformed_id(client):
    response = await client.get("/employees/EMP@#$")
    assert response.status_code == 422


async def test_get_employee_by_id_returns_422_on_whitespace_id(client):
    response = await client.get("/employees/%20")
    assert response.status_code == 422


async def test_get_employee_by_id_returns_422_on_sql_injection_string(client):
    response = await client.get("/employees/' OR '1'='1")
    assert response.status_code == 422


# ── Edge ─────────────────────────────────────────────────────────────────────

async def test_get_employee_by_id_with_24_char_hex_but_nonexistent_returns_404(client):
    response = await client.get("/employees/507f1f77bcf86cd799439011")
    assert response.status_code == 404
