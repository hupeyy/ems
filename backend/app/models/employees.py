from datetime import datetime, timezone
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field

StatusLiteral = Literal["Active", "Inactive", "On Leave", "Terminated", "Retired"]
class Employee(BaseModel):
    employeeId: str
    name: str
    email: EmailStr
    department: str
    position: str
    status: StatusLiteral = "Active"

class EmployeeCreate(Employee):
    employeeId: str = Field(..., examples=["EMP12345"])
    name: str = Field(..., min_length=1, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    department: str = Field(..., examples=["Engineering"])
    position: str = Field(..., examples=["Software Engineer"])
    status: StatusLiteral = Field("Active", examples=["Active"])
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), examples=["2024-06-01T12:00:00Z"])


class EmployeeUpdate(Employee):
    employeeId: Optional[str] = Field(None, examples=["EMP12345"])
    name: Optional[str] = Field(None, min_length=1, examples=["John Doe"])
    email: Optional[EmailStr] = Field(None, examples=["john.doe@example.com"])
    department: Optional[str] = Field(None, examples=["Engineering"])
    position: Optional[str] = Field(None, examples=["Software Engineer"])
    status: Optional[StatusLiteral] = Field(None, examples=["Active"])
    updatedAt: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), examples=["2024-06-01T12:00:00Z"])


class EmployeeResponse(Employee):
    employeeId: str
    name: str
    email: EmailStr
    department: str
    position: str
    status: StatusLiteral = "Active"
    createdAt: datetime