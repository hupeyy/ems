from fastapi import APIRouter, Depends, status
from app.models.users import UserCreate, UserResponse, UserInDB, ActivityLogEntry
from app.repository.users import UserRepository
from app.auth.utils import hash_password 
from app.dependencies.users import get_user_repository
from datetime import datetime, timezone

class AuthController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, payload: UserCreate) -> UserResponse:
        hashed_password = hash_password(payload.password)
        activity_log_entry = ActivityLogEntry(action="register", timestamp=datetime.now(timezone.utc))
        user = UserInDB(role="user", email=payload.email, hashed_password=hashed_password, activity_log=[activity_log_entry])
        user_id = await self.user_repository.create_user(user)

        return UserResponse(id=str(user_id), email=payload.email, role=user.role)

def get_auth_controller(user_repo: UserRepository = Depends(get_user_repository)) -> AuthController:
    return AuthController(user_repo)