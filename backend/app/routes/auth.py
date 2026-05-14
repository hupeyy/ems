from fastapi import APIRouter, Depends, status
from app.models.users import UserCreate, UserResponse
from app.controller.auth import AuthController, get_auth_controller 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(payload: UserCreate, controller: AuthController = Depends(get_auth_controller)) -> UserResponse:
    return await controller.register_user(payload)