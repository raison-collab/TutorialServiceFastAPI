import asyncio
from typing import AsyncGenerator

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.testclient import TestClient

from config import DB_USER_TEST, DB_PASSWORD_TEST, DB_HOST_TEST, DB_NAME_TEST
from main import app
from src.auth.database import Base as AuthBase, get_async_session

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"

engine = create_async_engine(DATABASE_URL_TEST)

AuthBase.metadata.bind = engine

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(AuthBase.metadata.create_all)
        trans = await conn.begin_nested()
        yield  # Здесь выполняются ваши тесты
        await trans.rollback()


@pytest.fixture(scope="session")
async def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture
async def async_gen_fixture():
    async def gen_obj():
        yield "example"

    yield gen_obj()


async def async_finalizer(gen_obj):
    try:
        await gen_obj.__anext__()
    except StopAsyncIteration:
        pass
    else:
        msg = "Async generator fixture didn't stop."
        msg += "Yield only once."
        raise ValueError(msg)
