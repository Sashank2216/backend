# schemas/brand_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class BrandCreateUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    tag: Optional[str]
    location: Optional[str]
    event_start: Optional[date]
    event_end: Optional[date]

class BrandOut(BaseModel):
    id: str
    user_id: str
    name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    tag: Optional[str]
    location: Optional[str]
    event_start: Optional[date]
    event_end: Optional[date]

    class Config:
        from_attributes = True
