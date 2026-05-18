from app.models.users import ActivityLogEntry, UserCreate, UserResponse, UserInDB
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def create_user(self, user: UserInDB) -> str:
        try:
            result = await self.collection.insert_one(user.model_dump(exclude={"id"}))
        except DuplicateKeyError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
        return str(result.inserted_id)

    async def get_user_by_email(self, email: str) -> UserInDB | None:
        user_data = await self.collection.find_one({"email": email})
        if user_data:
            return UserInDB(**user_data)
        return None
    
    async def append_activity_log(self, email: str, entry: ActivityLogEntry) -> None:
        await self.collection.update_one(
            {"email": email},
            {"$push": {"activity_log": entry.model_dump()}}
        )