# schemas/brand_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from datetime import datetime

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

class BrandFullOut(BaseModel):
    # User table fields
    user_id: str
    user_name: str
    user_email: EmailStr
    user_tag: Optional[str]
    user_location: Optional[str]
    user_role: str
    user_created_at: Optional[datetime]

    # Brand table fields
    brand_id: str
    brand_name: Optional[str]
    brand_email: Optional[EmailStr]
    phone_number: Optional[str]
    brand_tag: Optional[str]
    brand_location: Optional[str]
    event_start: Optional[date]
    event_end: Optional[date]

    class Config:
        from_attributes = True
