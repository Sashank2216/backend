# schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    tag: Optional[str] = None
    location: Optional[str] = None
    role: str  # 'brand' or 'influencer'

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    tag: Optional[str]
    location: Optional[str]
    role: str

    class Config:
        from_attributes = True
