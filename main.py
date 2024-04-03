import psycopg2
import uvicorn
from starlette.staticfiles import StaticFiles

from config import DEBUG, SERVER_HOST, SERVER_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_CONNECTION_TIMES
from loader import app, fastapi_users, admin
from src.admin.admin import RoleAdmin, UserAdmin, SubjectAdmin, ServiceAdmin, OrderAdmin, StatusAdmin
from src.main_service.routers import router as main_router
from src.pages.routers import router as pages_router
from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate


def check_postgres_connection():
    try:
        print('db-url ', DB_HOST, DB_PORT)

        connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

        cursor = connection.cursor()

        cursor.execute("SELECT 1")

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return True

    except Exception as e:
        return False


def try_connect_to_database():
    connection_times = 1
    while not check_postgres_connection():
        if connection_times == DB_CONNECTION_TIMES:
            raise ConnectionError("Timeout. Не получилось подключиться к Postgres")

        print(f"Пробую подключиться к Postgres. {connection_times=}")
        connection_times += 1

    print(f"Успешно подключен к Postgres. {connection_times=}")


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
    admin.add_view(SubjectAdmin)
    admin.add_view(ServiceAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(StatusAdmin)


if __name__ == "__main__":
    # подключение к базе данных
    try_connect_to_database()

    # подкючение роутеров и регистрация моделей в админке
    include_routers()
    register_admin_models()

    if DEBUG:
        uvicorn.run(app)
    else:
        uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
