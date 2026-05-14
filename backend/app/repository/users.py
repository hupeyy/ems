from app.models.users import ActivityLogEntry, UserCreate, UserResponse, UserInDB
from motor.motor_asyncio import AsyncIOMotorDatabase

class DuplicateEmailError(Exception):
    pass

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def create_user(self, user: UserInDB) -> str:

        existing_user = await self.collection.find_one({"email": user.email})
        if existing_user is not None:
            raise DuplicateEmailError(f"Email {user.email} is already registered")


        result = await self.collection.insert_one(user.model_dump())
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