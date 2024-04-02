from typing import Any

from sqlalchemy import select, delete, update

from loader import async_session_maker

from .database import Role


class DBService:
    def __init__(self):
        self.session = async_session_maker()

    async def create_role(self, data: dict[str, Any]):
        self.session.add(Role(**data))

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

    async def update_role(self, role_id: int, data: dict[str, Any]):
        await self.session.execute(update(Role).where(Role.id == role_id).values(**data))
