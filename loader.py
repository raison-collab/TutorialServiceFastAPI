"""
Для инициализации переменных для избежания проблем с импортами
"""
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from sqladmin import Admin
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DEBUG, DATABASE_URL
from src.auth.auth import auth_backend
from src.auth.database import User
from src.auth.manager import get_user_manager

#######################################################
# FASTAPI
#######################################################


########################################################
# DATABASE
########################################################
# create engine for db
engine = create_async_engine(DATABASE_URL)

# session
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

########################################################
# REGISTRATION AND AUTH FASTAPIUSERS
########################################################
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

########################################################
# ADMIN
########################################################

