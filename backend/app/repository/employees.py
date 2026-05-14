from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.employees import EmployeeCreate, EmployeeUpdate

class EmployeeRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, payload: EmployeeCreate) -> dict:
        employee = payload.model_dump()
        result = await self.db.employees.insert_one(employee)
        employee["_id"] = str(result.inserted_id)
        return employee

    async def find_all(self) -> list[dict]:
        cursor = self.db.employees.find()
        return await cursor.to_list(length=None)

    async def find_by_employeeId(self, employeeId: str) -> dict | None:
        return await self.db.employees.find_one({"employeeId": employeeId})

    async def update(self, employeeId: str, payload: EmployeeUpdate) -> dict | None:
        updates = payload.model_dump(exclude_none=True)
        updates["updatedAt"] = datetime.now(timezone.utc)
        result = await self.db.employees.find_one_and_update(
            {"employeeId": employeeId},
            {"$set": updates},
            return_document=True,
        )
        return result

    async def delete(self, employeeId: str) -> bool:
        result = await self.db.employees.delete_one({"employeeId": employeeId})
        return result.deleted_count == 1