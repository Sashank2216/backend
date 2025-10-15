# models/brand.py
import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from database import Base

class Brand(Base):
    __tablename__ = "brands"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String(100), nullable=True)
    email = Column(String(120), nullable=True)
    phone_number = Column(String(20), nullable=True)
    tag = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    event_start = Column(Date, nullable=True)
    event_end = Column(Date, nullable=True)
