from fastapi import APIRouter, Depends, Path, status
from app.models.employees import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.controller.employees import EmployeeController
from app.dependencies import get_employee_controller

router = APIRouter(prefix="/employees")

_ID = Path(..., min_length=1, pattern=r"^[A-Za-z0-9_-]+$")

@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(payload: EmployeeCreate,
                          controller: EmployeeController = Depends(get_employee_controller)
) -> EmployeeResponse:
    return await controller.create_employee(payload)

@router.get("", status_code=status.HTTP_200_OK, response_model=list[EmployeeResponse])
async def get_employees(controller: EmployeeController = Depends(get_employee_controller)
) -> list[EmployeeResponse]:
    return await controller.get_all_employees()

@router.get("/{employeeId}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def get_employee(employeeId: str = _ID,
                       controller: EmployeeController = Depends(get_employee_controller)
) -> EmployeeResponse:
    return await controller.get_employee(employeeId)

@router.put("/{employeeId}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def update_employee(employeeId: str = _ID,
                          payload: EmployeeUpdate = ...,
                          controller: EmployeeController = Depends(get_employee_controller)
) -> EmployeeResponse:
    return await controller.update_employee(employeeId, payload)

@router.delete("/{employeeId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employeeId: str = _ID,
                          controller: EmployeeController = Depends(get_employee_controller)
) -> None:
    await controller.delete_employee(employeeId)