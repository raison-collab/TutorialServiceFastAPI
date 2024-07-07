import random

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope='session')
async def test_roles(ac: AsyncClient):
    login_res = await ac.post("/api/auth/jwt/login", data={
        "username": "adminunique@example.com",
        "password": "string"
    })

    assert login_res.status_code == 200, f"Ошибка авторизации: {login_res.status_code}"

    access_token = login_res.json()["access_token"]

    response = await ac.get("/api/roles", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200, "Invalid request"
    assert len(response.json()) > 0


@pytest.mark.asyncio(scope='session')
async def test_add_status(ac: AsyncClient):
    st = "абвгдежзийклмнопрстуфхцч"
    res = await ac.post("/api/status", json={
        "name": st[random.randint(0, len(st))]
    })

    assert res.status_code == 200, "Invalid request"


@pytest.mark.asyncio(scope='session')
async def test_subjects(ac: AsyncClient):
    login_res = await ac.post("/api/auth/jwt/login", data={
        "username": "adminunique@example.com",
        "password": "string"
    })

    assert login_res.status_code == 200, f"Ошибка авторизации: {login_res.status_code}"

    access_token = login_res.json()["access_token"]

    response = await ac.get("/api/subjects", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200, "Invalid request"
    assert len(response.json()) != 0
