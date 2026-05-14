import pytest
from pydantic import ValidationError

from app.models.employees import Employee, EmployeeCreate, EmployeeUpdate


def test_employee_model_imports_and_validates_minimal_payload():
    emp = Employee(
        employeeId="EMP001",
        name="John Doe",
        email="john.doe@example.com",
        department="Engineering",
        position="Software Engineer",
    )
    assert emp.employeeId == "EMP001"
    assert emp.status == "Active"  # default value


def test_employee_create_rejects_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        EmployeeCreate(
            employeeId="EMP001",
            name="John Doe",
            email="not-an-email",
            department="Engineering",
            position="Software Engineer",
        )
    errors = exc_info.value.errors()
    assert any("email" in str(e["loc"]) for e in errors)


def test_employee_update_allows_all_optional_fields_none():
    update = EmployeeUpdate(name="John Doe")
    assert update.email is None
    assert update.department is None
    assert update.position is None
    assert update.status is None
