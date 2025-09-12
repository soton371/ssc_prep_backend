
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    profile_image: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: str
    profile_image: Optional[str] = None

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = "bearer"

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: Optional[int] = None

    class Config:
        from_attributes = True
