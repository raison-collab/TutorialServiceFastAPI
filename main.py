import psycopg2
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqladmin import Admin
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import DEBUG, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_CONNECTION_TIMES, FRONTEND_URL
from loader import fastapi_users, engine
from sql_start_scripts.sql_scripts import save_data
from src.admin.admin import RoleAdmin, UserAdmin, SubjectAdmin, ServiceAdmin, OrderAdmin, StatusAdmin
from src.auth.auth import auth_backend
from src.auth.routers import router as auth_router
from src.auth.schemas import UserRead, UserCreate
from src.main_service.routers import router as main_router

app = FastAPI(
    title="Tutoring Service",
    debug=DEBUG,
)

# cors чтобы связать фронт и бэк
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(app, engine, templates_dir='admin_templates', debug=DEBUG)


# Подключение обработчика ошибок валидации
@app.exception_handler(ValidationError)
async def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()}),
    )


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
    # Основные конечные точки
    app.include_router(main_router)

    app.include_router(auth_router)

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


def main():
    # подключение к базе данных
    try_connect_to_database()

    # подкючение роутеров и регистрация моделей в админке
    include_routers()
    register_admin_models()

    # Заполняю базу данных необходимыми данными
    save_data()


main()
