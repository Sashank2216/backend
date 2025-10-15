# models/user.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.mysql import CHAR
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    tag = Column(String(50), nullable=True)      # initial tag from signup
    location = Column(String(100), nullable=True) # initial location from signup
    role = Column(Enum("brand", "influencer"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
