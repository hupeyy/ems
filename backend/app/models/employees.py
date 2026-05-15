from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator

# Request/Response patterns for Employees collection

class Employee(BaseModel):
    employeeId: str
    name: str
    email: EmailStr
    department: str
    position: str
    status: str = "Active"

class EmployeeCreate(BaseModel):
    employeeId: str = Field(..., examples=["EMP12345"])
    name: str = Field(..., min_length=1, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    department: str = Field(..., examples=["Engineering"])
    position: str = Field(..., examples=["Software Engineer"])
    status: str = Field("Active", examples=["Active"])
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), examples=["2024-06-01T12:00:00Z"])


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, examples=["John Doe"])
    email: Optional[EmailStr] = Field(None, examples=["john.doe@example.com"])
    department: Optional[str] = Field(None, examples=["Engineering"])
    position: Optional[str] = Field(None, examples=["Software Engineer"])
    status: Optional[str] = Field(None, examples=["Active"])

    @model_validator(mode="before")
    @classmethod
    def at_least_one_field_required(cls, values: dict) -> dict:
        if isinstance(values, dict) and not any(v is not None for v in values.values()):
            raise ValueError("At least one field must be provided for update")
        return values


class EmployeeResponse(BaseModel):
    employeeId: str
    name: str
    email: EmailStr
    department: str
    position: str
    status: str = "Active"
    createdAt: datetime