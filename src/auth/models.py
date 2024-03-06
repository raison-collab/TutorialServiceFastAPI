from pydantic import BaseModel
from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean
from sqlalchemy.orm import mapped_column

metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('email', String, nullable=False, index=True, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)
