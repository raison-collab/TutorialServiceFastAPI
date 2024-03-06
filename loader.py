"""
Для инициализации переменных для избежания проблем с импортами
"""
from fastapi_users import FastAPIUsers

from src.auth.auth import auth_backend
from src.auth.database import User
from src.auth.manager import get_user_manager

# init FastAPIUses
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
