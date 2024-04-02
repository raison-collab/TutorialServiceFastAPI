from typing import Any

from sqlalchemy import select, delete, update

from loader import async_session_maker
from .models import StatusModel, SubjectModel, ServiceModel, OrderModel


# todo Объекты с одинаковыми именами
# todo поработать с возвращением нужных значений и выбрасыванимем ошибок

class DBService:
    def __init__(self):
        self.session = async_session_maker()

    async def create_status(self, status_data: dict):
        """
        Создает статус
        :param status_data:
        :return:
        """
        self.session.add(StatusModel(**status_data))

    async def get_statuses(self) -> list[dict[str, Any]]:
        """
        Получает список статусов
        :return:
        """
        res = await self.session.execute(select(StatusModel))
        return [{"id": el[0].id, "name": el[0].name} for el in res.fetchall()]

    async def get_status_by_id(self, id: int) -> dict[str, Any]:
        """
        Получает статус по ID
        :param id:
        :return:
        """
        res = await self.session.execute(select(StatusModel).where(StatusModel.id == id))
        row = res.fetchone()
        if not row:
            return {}

        return {"id": row[0].id, "name": row[0].name}

    async def update_status(self, status_id: int, status_data: dict[str, Any]):
        """
        Обновляет статус
        :param status_id:
        :param status_data:
        :return:
        """
        await self.session.execute(update(StatusModel).where(StatusModel.id == status_id).values(**status_data))

    async def delete_status(self, status_id: int):
        """
        Удаляет статус
        :param status_id:
        :return:
        """
        await self.session.execute(delete(StatusModel).where(StatusModel.id == status_id))

    async def create_subject(self, subject_data: dict):
        """
        Создает предмет
        :param subject_data:
        :return:
        """
        self.session.add(SubjectModel(**subject_data))

    async def get_subjects(self) -> list[dict[str, Any]]:
        """
        Получает список предметов
        :return:
        """
        res = await self.session.execute(select(SubjectModel))
        return [{"id": el[0].id, "name": el[0].name} for el in res.fetchall()]

    async def get_subject_by_id(self, id: int) -> dict[str, Any]:
        """
        Получает предмет по ID
        :param id:
        :return:
        """
        res = await self.session.execute(select(SubjectModel).where(SubjectModel.id == id))
        row = res.fetchone()
        if not row:
            return {}

        return {"id": row[0].id, "name": row[0].name}

    async def update_subject(self, subject_id: int, subject_data: dict[str, Any]):
        """
        Обновляет предмет
        :param subject_id:
        :param subject_data:
        :return:
        """
        await self.session.execute(update(SubjectModel).where(SubjectModel.id == subject_id).values(**subject_data))

    async def delete_subject(self, subject_id: int):
        """
        Удаляет предмет
        :param subject_id:
        :return:
        """
        await self.session.execute(delete(SubjectModel).where(SubjectModel.id == subject_id))

    async def create_service(self, service_data: dict[str, Any]):
        """
        создает сервис
        :param service_data:
        :return:
        """
        self.session.add(ServiceModel(**service_data))

    async def get_service_by_id(self, service_id: int) -> dict[str, Any]:
        """
        получает сервис по ID
        :param service_id:
        :return:
        """
        res = await self.session.execute(select(ServiceModel).where(ServiceModel.id == service_id))
        row = res.fetchone()

        if not row:
            return {}

        return {"id": row[0].id, "subject_id": row[0].subject_id, "user_id": row[0].user_id, "amount": row[0].amount,
                "info": row[0].info}

    async def get_services(self) -> list[dict[str, Any]]:
        """
        Получает список сервисов
        :return:
        """
        res = await self.session.execute(select(ServiceModel))
        return [{"id": row[0].id, "subject_id": row[0].subject_id, "user_id": row[0].user_id, "amount": row[0].amount,
                 "info": row[0].info} for row in res.fetchall()]

    async def update_service(self, service_data: dict[str, Any], service_id: int):
        """
        Обновляет сервис
        :param service_data:
        :param service_id:
        :return:
        """
        await self.session.execute(update(ServiceModel).where(ServiceModel.id == service_id).values(**service_data))

    async def delete_service(self, service_id: int):
        """
        Удаляет сервис
        :param service_id:
        :return:
        """
        await self.session.execute(delete(ServiceModel).where(ServiceModel.id == service_id))

    async def create_order(self, data: dict[str, Any]):
        """
        Создает заказ
        :param data:
        :return:
        """
        self.session.add(OrderModel(**data))

    async def get_order_by_id(self, order_id: int) -> dict[str, Any]:
        """
        Получает заказ по ID
        :param order_id:
        :return:
        """
        res = await self.session.execute(select(OrderModel).where(OrderModel.id == order_id))
        row = res.fetchone()

        if not row:
            return {}

        return {"id": row[0].id, "service_id": row[0].service_id, "user_id": row[0].user_id, "status_id": row[0].status_id}

    async def get_orders(self) -> list[dict[str, Any]]:
        """
        Получает все заказы
        :return:
        """
        res = await self.session.execute(select(OrderModel))
        return [{"id": row[0].id, "service_id": row[0].service_id, "user_id": row[0].user_id, "status_id": row[0].status_id} for row in res.fetchall()]

    async def update_order(self, order_id: int, data: dict[str, Any]):
        """
        Обновляет заказ
        :param order_id:
        :param data:
        :return:
        """
        await self.session.execute(update(OrderModel).where(OrderModel.id == order_id).values(**data))

    async def delete_order(self, order_id: int):
        """
        Удаляет заказ
        :param order_id:
        :return:
        """
        await self.session.execute(delete(OrderModel).where(OrderModel.id == order_id))
