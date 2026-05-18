from fastapi import APIRouter, Depends, status, HTTPException, Request
from app.models.users import UserCreate, UserResponse, UserInDB, ActivityLogEntry, LoginRequest, LoginResponse
from app.repository.users import UserRepository
from app.auth.utils import hash_password, verify_password, create_access_token
from datetime import datetime, timezone
from jose import JWTError, jwt

class AuthController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, payload: UserCreate) -> UserResponse:
        existing_user = await self.user_repository.get_user_by_email(payload.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
        hashed_password = hash_password(payload.password)
        activity_log_entry = ActivityLogEntry(action="register", timestamp=datetime.now(timezone.utc))
        user = UserInDB(
            role="user",
            email=payload.email,
            hashed_password=hashed_password,
            activity_log=[activity_log_entry]
        )
        user_id = await self.user_repository.create_user(user)

        if not user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")

        return UserResponse(id=str(user_id), email=payload.email, role=user.role)
    
    async def login_user(self, payload: LoginRequest) -> LoginResponse:
        user = await self.user_repository.get_user_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        await self.user_repository.append_activity_log(payload.email, ActivityLogEntry(action="login", timestamp=datetime.now(timezone.utc))) 

        token = create_access_token(email=user.email, role=user.role)
        return LoginResponse(access_token=token)

    async def me(self, current_user: UserInDB) -> UserResponse:
        await self.user_repository.append_activity_log(current_user.email, ActivityLogEntry(action="me", timestamp=datetime.now(timezone.utc)))
        return UserResponse(id=str(current_user.id), email=current_user.email, role=current_user.role)

