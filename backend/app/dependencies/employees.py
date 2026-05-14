# FastAPI dependency injection for EmployeeController and EmployeeRepository

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.controller.employees import EmployeeController
from app.repository.employees import EmployeeRepository
from app.db.mongo_db import get_db


async def get_employee_db() -> AsyncIOMotorDatabase:
    return await get_db()


async def get_employee_repository(db: AsyncIOMotorDatabase = Depends(get_employee_db)) -> EmployeeRepository:
    return EmployeeRepository(db)


async def get_employee_controller(repo: EmployeeRepository = Depends(get_employee_repository)) -> EmployeeController:
    return EmployeeController(repo)