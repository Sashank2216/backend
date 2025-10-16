# schemas/influencer_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class InfluencerCreateUpdate(BaseModel):
    reach: Optional[int] = 0
    verified: Optional[bool] = False
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    tag: Optional[str] = None
    location: Optional[str] = None

class InfluencerOut(BaseModel):
    id: str
    user_id: str
    reach: int
    verified: bool
    email: Optional[EmailStr]

    class Config:
        from_attributes = True

class InfluencerFullOut(BaseModel):
    # User table fields
    user_id: str
    user_name: str
    user_email: EmailStr
    user_tag: Optional[str]
    user_location: Optional[str]
    user_role: str
    user_created_at: Optional[datetime]

    # Influencer table fields
    influencer_id: str
    reach: int
    verified: bool
    influencer_email: Optional[EmailStr]

    class Config:
        from_attributes = True
