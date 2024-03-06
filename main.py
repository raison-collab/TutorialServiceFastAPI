from fastapi import FastAPI

from config import DEBUG
from loader import fastapi_users
from src.main_service.routers import router as main_router
from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="Tutoring Service",
    debug=DEBUG
)

# Основные конечные точки
app.include_router(main_router)

# Авторизация
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Регистрация
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
