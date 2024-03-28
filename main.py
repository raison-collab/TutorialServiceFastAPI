import uvicorn
from starlette.staticfiles import StaticFiles

from config import DEBUG, SERVER_HOST, SERVER_PORT
from loader import app, fastapi_users, admin
from src.admin.admin import RoleAdmin, UserAdmin
from src.main_service.routers import router as main_router
from src.pages.routers import router as pages_router
from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate


def include_routers():
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


def register_admin_models():
    admin.add_view(RoleAdmin)
    admin.add_view(UserAdmin)


if __name__ == "__main__":
    include_routers()
    register_admin_models()

    if DEBUG:
        uvicorn.run(app)
    else:
        uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
