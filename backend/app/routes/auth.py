from fastapi import APIRouter, Depends, status, HTTPException, Request
from app.models.users import UserCreate, UserResponse, LoginRequest, LoginResponse, UserInDB, UserRole
from app.controller.auth import AuthController 
from app.dependencies.users import get_current_user, get_auth_controller

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(payload: UserCreate, controller: AuthController = Depends(get_auth_controller)) -> UserResponse:
    return await controller.register_user(payload)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login_user(payload: LoginRequest, controller: AuthController = Depends(get_auth_controller)) -> LoginResponse:
    return await controller.login_user(payload)

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def me(current_user: UserInDB = Depends(get_current_user), controller: AuthController = Depends(get_auth_controller)) -> UserResponse:
    return await controller.me(current_user)
