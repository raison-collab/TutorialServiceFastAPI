import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config import DEBUG
from loader import fastapi_users
from src.main_service.routers import router as main_router
from src.pages.routers import router as pages_router
from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="Tutoring Service",
    debug=DEBUG
)

# include static files
app.mount('/static', StaticFiles(directory='static'), name='static')

# pages router
app.include_router(pages_router)

# Основные конечные точки
app.include_router(main_router)

# Авторизация
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)

# Регистрация
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)

if __name__ == "__main__":
    uvicorn.run(app)
