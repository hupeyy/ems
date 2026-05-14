from typing import Literal
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from datetime import datetime, timezone

UserRole = Literal["admin", "user"]

class UserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=64) 
    password: str = Field(min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: UserRole

class ActivityLogEntry(BaseModel):
    action: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    detail: str | None = None

class UserInDB(BaseModel):
    id: str | None = None
    email: EmailStr
    hashed_password: str
    role: UserRole = "user"
    activity_log: list[ActivityLogEntry] = Field(default_factory=list)