import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from src.auth.database import Role
from tests.conftest import async_session_maker


@pytest.mark.asyncio(scope='session')
async def test_add_role():

    async with async_session_maker() as session:
        try:
            await session.execute(
                insert(Role).values(id=1, name="Ученик")
            )

            await session.execute(
                insert(Role).values(id=2, name="Учитель")
            )

            await session.commit()
        except IntegrityError:
            await session.rollback()

        res = await session.execute(
            select(Role)
        )

        roles = res.scalars().all()

        assert len(roles) == 2
        assert roles[0].id == 1
        assert roles[0].name == "Ученик"
        assert roles[1].id == 2
        assert roles[1].name == "Учитель"


@pytest.mark.asyncio(scope='session')
async def test_basic_user_register(ac: AsyncClient):
    res = await ac.post("/api/auth/register", json={
        "email": "userunique@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "first_name": "string",
        "second_name": "string",
        "last_name": "string",
        "card_number": "string",
        "role_id": 1
    })

    res_admin = await ac.post("/api/auth/register", json={
        "email": "adminunique@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "first_name": "string",
        "second_name": "string",
        "last_name": "string",
        "card_number": "string",
        "role_id": 2
    })

    if res.status_code == 400 or res_admin.status_code == 400:
        assert res.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"
    else:
        assert res.status_code == 201, "Request Error"
        assert res_admin.status_code == 201, "Request Error"

        res_json = res.json()
        res_admin_json = res.json()

        assert res_json["email"] == "userunique@example.com", "Invalid email"
        assert res_admin_json["email"] == "adminunique@example.com", "Invalid admin email"
        assert res_json["role_id"] == 1, "Invalid role_id"
        assert res_admin_json["role_id"] == 2, "Invalid admin role_id"


@pytest.mark.asyncio(scope='session')
async def test_basic_user_login(ac: AsyncClient):
    res = await ac.post("/api/auth/jwt/login", data={
        "username": "userunique@example.com",
        "password": "string"
    })

    assert res.status_code == 200, "Request Error"

    assert res.json()["access_token"] != "", "Invalid token"


@pytest.mark.asyncio(scope='session')
async def test_admin_user_login(ac: AsyncClient):
    res = await ac.post("/api/auth/jwt/login", data={
        "username": "adminunique@example.com",
        "password": "string"
    })

    assert res.status_code == 200, "Request Error"

    assert res.json()["access_token"] != "", "Invalid token"
