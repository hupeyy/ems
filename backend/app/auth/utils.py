from fastapi import HTTPException, status, Depends, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.settings import settings
from datetime import datetime, timezone, timedelta
from app.repository.users import UserRepository
from app.models.users import UserInDB

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(email: str, role: str) -> str:
    payload = {
        "sub": email,
        "role": role, 
        "iat": datetime.now(timezone.utc), 
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    } 
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

