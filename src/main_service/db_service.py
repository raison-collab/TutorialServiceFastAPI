from typing import Any

from sqlalchemy import select, delete, update

from loader import async_session_maker
from .errors import AlreadyExistsError
from .models import StatusModel, SubjectModel, ServiceModel, OrderModel


class DBService:
    def __init__(self):
        self.session = async_session_maker()

    async def create_status(self, status_data: dict):
        """
        Создает статус
        :param status_data:
        :return:
        """
        is_exists = [el for el in await self.get_statuses() if el["name"] == status_data["name"]]
        status = StatusModel(**status_data)
        if is_exists:
            raise AlreadyExistsError("Статус с таким названием уже есть")

        self.session.add(status)
        await self.session.commit()

        return status

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

    async def update_status(self, status_id: int, status_data: dict[str, Any]) -> StatusModel:
        """
        Обновляет статус
        :param status_id:
        :param status_data:
        :return:
        """
        status = StatusModel(**status_data)
        await self.session.execute(update(StatusModel).where(StatusModel.id == status_id).values(**status_data))
        await self.session.commit()
        return status

    async def delete_status(self, status_id: int) -> int:
        """
        Удаляет статус
        :param status_id:
        :return:
        """
        await self.session.execute(delete(StatusModel).where(StatusModel.id == status_id))
        await self.session.commit()
        return status_id

    async def create_subject(self, subject_data: dict) -> SubjectModel:
        """
        Создает предмет
        :param subject_data:
        :return:
        """
        is_exists = [el for el in await self.get_subjects() if el["name"] == subject_data["name"]]
        if is_exists:
            raise AlreadyExistsError('Предмет с таким именем уже есть')

        subject = SubjectModel(**subject_data)
        self.session.add(subject)
        await self.session.commit()
        return subject

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

    async def update_subject(self, subject_id: int, subject_data: dict[str, Any]) -> SubjectModel:
        """
        Обновляет предмет
        :param subject_id:
        :param subject_data:
        :return:
        """
        subject = SubjectModel(**subject_data)

        await self.session.execute(update(SubjectModel).where(SubjectModel.id == subject_id).values(**subject_data))
        await self.session.commit()

        return subject

    async def delete_subject(self, subject_id: int) -> int:
        """
        Удаляет предмет
        :param subject_id:
        :return:
        """
        await self.session.execute(delete(SubjectModel).where(SubjectModel.id == subject_id))
        await self.session.commit()

        return subject_id

    async def create_service(self, service_data: dict[str, Any]) -> ServiceModel:
        """
        создает сервис
        :param service_data:
        :return:
        """
        is_exists = [el for el in await self.get_services() if el == service_data]
        service = ServiceModel(**service_data)
        if is_exists:
            raise AlreadyExistsError("Услуга с такими данными уже существует")

        self.session.add(service)
        await self.session.commit()
        return service

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

    async def update_service(self, service_data: dict[str, Any], service_id: int) -> ServiceModel:
        """
        Обновляет сервис
        :param service_data:
        :param service_id:
        :return:
        """
        service = ServiceModel(**service_data)
        await self.session.execute(update(ServiceModel).where(ServiceModel.id == service_id).values(**service_data))
        await self.session.commit()
        return service

    async def delete_service(self, service_id: int) -> int:
        """
        Удаляет сервис
        :param service_id:
        :return:
        """
        await self.session.execute(delete(ServiceModel).where(ServiceModel.id == service_id))
        await self.session.commit()
        return service_id

    async def create_order(self, data: dict[str, Any]) -> OrderModel:
        """
        Создает заказ
        :param data:
        :return:
        """
        is_exists = [el for el in await self.get_statuses() if el == data]
        order = OrderModel(**data)
        if is_exists:
            raise AlreadyExistsError("Заказ с такими данными уже существует")

        self.session.add(order)
        await self.session.commit()
        return order

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

    async def update_order(self, order_id: int, data: dict[str, Any]) -> OrderModel:
        """
        Обновляет заказ
        :param order_id:
        :param data:
        :return:
        """
        order = OrderModel(**data)
        await self.session.execute(update(OrderModel).where(OrderModel.id == order_id).values(**data))
        await self.session.commit()
        return order

    async def delete_order(self, order_id: int) -> int:
        """
        Удаляет заказ
        :param order_id:
        :return:
        """
        await self.session.execute(delete(OrderModel).where(OrderModel.id == order_id))
        await self.session.commit()
        return order_id
