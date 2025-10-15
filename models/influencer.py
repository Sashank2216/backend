# models/influencer.py
import uuid
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from database import Base

class Influencer(Base):
    __tablename__ = "influencers"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False, unique=True)
    reach = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    email = Column(String(120), nullable=True)
