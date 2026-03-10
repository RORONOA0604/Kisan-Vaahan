from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Base Config
class BaseConfig:
    from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    full_name: str
    is_active: bool
    user_type: str
    created_at: datetime

    class Config(BaseConfig):
        pass


class Signup(BaseModel):
    full_name: str
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    password: str
    user_type: Optional[str] = "buyer"   # expected: "buyer" or "farmer"

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    message: str
    data: dict | None = None

    class Config(BaseConfig):
        pass


# Token
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
