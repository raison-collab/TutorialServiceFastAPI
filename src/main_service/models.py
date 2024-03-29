from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import DeclarativeBase

from src.auth.database import User


class Base(DeclarativeBase):
    pass


class SubjectModel(Base):
    __tablename__ = "subject"
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name: str = Column(String(length=80), nullable=False)


class ServiceModel(Base):
    __tablename__ = "service"
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    subject_id: int = Column(Integer, ForeignKey("subject.id"))
    user_id: User = Column(Integer, ForeignKey(User.id))
    amount: float = Column(Float, nullable=False)
    info: str = Column(Text, nullable=False)


class OrderModel(Base):
    __tablename__ = "order"
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    service_id: int = Column(Integer, ForeignKey("service.id"))
    user_id: User = Column(Integer, ForeignKey(User.id))
    status_id: int = Column(Integer, ForeignKey("status.id"), nullable=False)


class StatusModel(Base):
    __tablename__ = "status"
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name: str = Column(String(length=85), nullable=False)
