from fastapi import Depends, HTTPException, status, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repository.users import UserRepository
from app.controller.auth import AuthController
from app.db.mongo_db import get_db
from app.models.users import UserInDB
from app.auth.utils import decode_access_token
from jose import JWTError, jwt

async def get_user_db() -> AsyncIOMotorDatabase:
    return await get_db()

async def get_user_repository(db: AsyncIOMotorDatabase = Depends(get_user_db)) -> UserRepository:
    return UserRepository(db)

def get_auth_controller(user_repo: UserRepository = Depends(get_user_repository)) -> AuthController:
    return AuthController(user_repo)

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Invalid credentials or missing token",
    headers = {"WWW-Authenticate": "Bearer"},
)

async def get_current_user(request: Request, user_repo: UserRepository = Depends(get_user_repository)) -> UserInDB:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise _CREDENTIALS_EXCEPTION
    token = auth_header.split(" ")[1]
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise _CREDENTIALS_EXCEPTION
        user = await user_repo.get_user_by_email(email)
        if user is None:
            raise _CREDENTIALS_EXCEPTION
        return user
    except JWTError:
        raise _CREDENTIALS_EXCEPTION