# schemas/influencer_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class InfluencerCreateUpdate(BaseModel):
    reach: Optional[int] = 0
    verified: Optional[bool] = False
    email: Optional[EmailStr] = None

class InfluencerOut(BaseModel):
    id: str
    user_id: str
    reach: int
    verified: bool
    email: Optional[EmailStr]

    class Config:
        from_attributes = True
