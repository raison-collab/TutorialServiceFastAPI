from pprint import pprint
from typing import Any

from sqlalchemy import select, delete, update

from loader import async_session_maker

from .database import Role, User
from .errors import AlreadyExistsError


class DBService:
    def __init__(self):
        self.session = async_session_maker()

    async def create_role(self, data: dict[str, Any]) -> Role:
        is_exists = [el for el in await self.get_roles() if el["name"] == data["name"]]
        if is_exists:
            raise AlreadyExistsError(f"Роль с именем {data['name']} уже существует")

        role: Role = Role(**data)
        self.session.add(role)
        await self.session.commit()
        return role

    async def get_roles(self) -> list[dict[str, Any]]:
        res = await self.session.execute(select(Role))
        return [{"id": row[0].id, "name": row[0].name} for row in res.fetchall()]

    async def get_role_by_id(self, role_id: int) -> dict[str, Any]:
        res = await self.session.execute(select(Role).where(Role.id == role_id))
        row = res.fetchone()

        if not row:
            return {}
        return {"id": row[0].id, "name": row[0].name}

    async def delete_role(self, role_id: int):
        await self.session.execute(delete(Role).where(Role.id == role_id))
        await self.session.commit()

    async def update_role(self, role_id: int, data: dict[str, Any]):
        await self.session.execute(update(Role).where(Role.id == role_id).values(**data))
        await self.session.commit()

    async def get_user_service_data(self, user_id: int) -> dict[str, Any]:
        res = await self.session.execute(select(User).where(User.id == user_id))
        row = res.fetchone()

        if not row:
            return {}
        return {
            "user_id": user_id,
            "f_name": row[0].first_name,
            "s_name": row[0].second_name,
            "l_name": row[0].last_name,
            "role_id": row[0].role_id
        }
