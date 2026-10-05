from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    id: int
    first_name: str
    last_name:str
    email: EmailStr



class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

class UpdateProfileRequest(BaseModel):
    first_name: str
    last_name: str