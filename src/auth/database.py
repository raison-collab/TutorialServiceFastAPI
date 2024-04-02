from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DATABASE_URL

# create engine for db
engine = create_async_engine(DATABASE_URL)

# session
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "role"
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name: str = Column(String(length=50), nullable=False)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    second_name: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    card_number: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    role_id: Role = Column(Integer, ForeignKey("role.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
