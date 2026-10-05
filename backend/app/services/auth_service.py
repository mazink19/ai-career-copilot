from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, RegisterResponse, LoginResponse, UpdateProfileRequest, UserResponse
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token



class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
    
    def register(self, request: RegisterRequest):
        existing_user = self.user_repository.get_by_email(request.email)
        if existing_user:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,detail="Email already exists")
        user = User(
            first_name = request.first_name,
            last_name = request.last_name,
            email = request.email,
            hashed_password = hash_password(request.password)
        )
        created_user = self.user_repository.create(user)
        return RegisterResponse(
            id = created_user.id,
            first_name = created_user.first_name,
            last_name = created_user.last_name,
            email = created_user.email,)
    

    def login(self, request: LoginRequest):
        user = self.user_repository.get_by_email(request.email)

        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
        )

        if not verify_password(request.password,user.hashed_password,):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
        )

        access_token = create_access_token(
        {"sub": str(user.id)})

        return LoginResponse(access_token=access_token)
    

    def get_current_user(self, user: User) -> UserResponse:
        
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,)
    
    
    def update_profile(self,current_user: User,
        request: UpdateProfileRequest,) -> UserResponse:

        current_user.first_name = request.first_name
        current_user.last_name = request.last_name

        updated_user = self.user_repository.update(current_user)

        return UserResponse(
        id=updated_user.id,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        email=updated_user.email,
    )