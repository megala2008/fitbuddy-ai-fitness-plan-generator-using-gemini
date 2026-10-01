from sqlalchemy import Column, Integer, String, Text
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    user_id = Column(String(100), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    weight = Column(String(30), nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(30), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)
