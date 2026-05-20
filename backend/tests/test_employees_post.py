VALID_EMPLOYEE = {
    "employeeId": "EMP00100",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "status": "Active"
}

EXPECTED_FIELDS = {"employeeId", "name", "email", "department", "position", "status", "createdAt", "updatedAt"}


# ── Happy Path ────────────────────────────────────────────────────────────────

async def test_post_employee_returns_201_with_id_and_shape(auth_admin_client):
    response = await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    assert response.status_code == 201
    assert EXPECTED_FIELDS == set(response.json().keys())
    data = response.json()
    assert data["employeeId"] == VALID_EMPLOYEE["employeeId"]
    assert data["name"] == VALID_EMPLOYEE["name"]
    assert data["email"] == VALID_EMPLOYEE["email"]
    assert data["department"] == VALID_EMPLOYEE["department"]
    assert data["position"] == VALID_EMPLOYEE["position"]
    assert data["status"] == VALID_EMPLOYEE["status"]


# ── Critical ──────────────────────────────────────────────────────────────────

async def test_post_employee_persists_document_to_db(auth_admin_client, test_db):
    await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)

    stored = await test_db.employees.find_one({"employeeId": VALID_EMPLOYEE["employeeId"]})
    assert stored is not None
    assert stored["employeeId"] == VALID_EMPLOYEE["employeeId"]
    assert stored["name"] == VALID_EMPLOYEE["name"]
    assert stored["email"] == VALID_EMPLOYEE["email"]
    assert stored["department"] == VALID_EMPLOYEE["department"]
    assert stored["position"] == VALID_EMPLOYEE["position"]
    assert stored["status"] == VALID_EMPLOYEE["status"]


async def test_post_employee_returns_409_on_duplicate_employee_id(auth_admin_client):
    await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    response = await auth_admin_client.post("/employees", json=VALID_EMPLOYEE)
    assert response.status_code == 409


# ── Negative ──────────────────────────────────────────────────────────────────

async def test_post_employee_returns_422_on_missing_required_field(auth_admin_client):
    payload = VALID_EMPLOYEE.copy()
    del payload["employeeId"]
    response = await auth_admin_client.post("/employees", json=payload)
    assert response.status_code == 422


async def test_post_employee_returns_422_on_invalid_email(auth_admin_client):
    payload = {**VALID_EMPLOYEE, "email": "not-an-email"}
    response = await auth_admin_client.post("/employees", json=payload)
    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]


async def test_post_employee_returns_422_on_name_too_short(auth_admin_client):
    payload = {**VALID_EMPLOYEE, "name": ""}
    response = await auth_admin_client.post("/employees", json=payload)
    assert response.status_code == 422
    assert "name" in response.json()["detail"][0]["loc"]


# ── Edge ─────────────────────────────────────────────────────────────────────

async def test_post_employee_defaults_status_to_active_when_omitted(auth_admin_client):
    payload = {k: v for k, v in VALID_EMPLOYEE.items() if k != "status"}
    response = await auth_admin_client.post("/employees", json=payload)
    assert response.status_code == 201
    assert response.json()["status"] == "Active"
