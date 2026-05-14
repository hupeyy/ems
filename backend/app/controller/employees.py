from fastapi import HTTPException, status

from app.models.employees import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.repository.employees import EmployeeRepository


class EmployeeController:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    async def create_employee(self, payload: EmployeeCreate) -> EmployeeResponse:
        existing_employee = await self.repo.find_by_employeeId(payload.employeeId)
        if existing_employee:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee with this employeeId already exists")
        employee = await self.repo.create(payload)
        return EmployeeResponse(**employee)

    async def get_all_employees(self) -> list[EmployeeResponse]:
        employees = await self.repo.find_all()
        return [EmployeeResponse(**e) for e in employees]

    async def get_employee(self, employeeId: str) -> EmployeeResponse:
        employee = await self.repo.find_by_employeeId(employeeId)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return EmployeeResponse(**employee)

    async def update_employee(self, employeeId: str, payload: EmployeeUpdate) -> EmployeeResponse:
        employee = await self.repo.update(employeeId, payload)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return EmployeeResponse(**employee)

    async def delete_employee(self, employeeId: str) -> None:
        deleted = await self.repo.delete(employeeId)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
