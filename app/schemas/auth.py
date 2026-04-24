from pydantic import BaseModel, EmailStr, validator

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Пароль должен быть не менее 8 символов')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

class WhoamiResponse(BaseModel):
    user: UserResponse

class MessageResponse(BaseModel):
    message: str