from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repository.users import UserRepository
from app.db.mongo_db import get_db

async def get_user_db() -> AsyncIOMotorDatabase:
    return await get_db()

async def get_user_repository(db: AsyncIOMotorDatabase = Depends(get_user_db)) -> UserRepository:
    return UserRepository(db)