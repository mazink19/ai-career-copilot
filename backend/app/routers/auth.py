from fastapi import APIRouter, Depends, status

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    UpdateProfileRequest,
    UserResponse,
)
from app.services.auth_service import AuthService
from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/register", response_model=RegisterResponse,
             status_code=status.HTTP_201_CREATED)

def register(request: RegisterRequest,
              service: AuthService= Depends(get_auth_service)):
    
    return service.register(request)


@router.post("/login")
def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    
    return service.login(request)


@router.get("/me",response_model=UserResponse,)
def me(current_user: User = Depends(get_current_user), service: AuthService = Depends(get_auth_service)):

    return service.get_current_user(current_user)

@router.patch("/me",  response_model=UserResponse)
def update_profile(
    request: UpdateProfileRequest, current_user: User= Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)):

    return service.update_profile(
        current_user, request
    )