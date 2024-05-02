from fastapi import APIRouter, Depends

from loader import fastapi_users
from src.auth.database import User
from .db_service import DBService
from .models import ServiceModel
from .schemas import *

router = APIRouter(
    prefix='/api',
    tags=['Main Api']
)

current_user = fastapi_users.current_user()
db_service = DBService()


@router.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@router.post("/subject", response_model=SubjectResponseSchema)
async def create_subject(data: SubjectSchema):
    res = await db_service.create_subject(data.dict())

    return {"id": res.id, 'name': res.name}


@router.get("/subjects", response_model=list[SubjectResponseSchema])
async def get_subjects(user: User = Depends(current_user)):
    return await db_service.get_subjects()


@router.get("/subject/{subject_id}", response_model=SubjectResponseSchema)
async def get_subject_by_id(subject_id: int):
    return await db_service.get_subject_by_id(subject_id)


@router.put("/subject/{subject_id}", response_model=SubjectResponseSchema)
async def update_subject(subject_id: int, data: SubjectSchema):
    return await db_service.update_subject(subject_id, data.dict())


@router.delete("/subject/{subject_id}", response_model=DeleteResponseSchema)
async def delete_subject(subject_id: int):
    res = await db_service.delete_subject(subject_id)

    return {"id": res}


@router.post('/service', response_model=ServiceResponseSchema)
async def create_service(data: ServiceSchema):
    res = await db_service.create_service(data.dict())

    return {
        'id': res.id,
        'subject_id': res.subject_id,
        'user_id': res.user_id,
        'amount': res.amount,
        'info': res.info,
    }


@router.get('/services', response_model=list[ServiceResponseSchema])
async def get_services(user: User = Depends(current_user)):
    return await db_service.get_services()


@router.get('/service/{service_id}', response_model=ServiceResponseSchema)
async def get_service_by_id(service_id: int):
    res = await db_service.get_service_by_id(service_id)

    return res


@router.put('/service/{service_id}', response_model=ServiceResponseSchema)
async def update_service(service_id: int, data: ServiceSchema):
    res: ServiceModel = await db_service.update_service(data.dict(), service_id)

    return {
        'id': res.id,
        'subject_id': res.subject_id,
        'user_id': res.user_id,
        'amount': res.amount,
        'info': res.info,
    }


@router.delete('/service/{service_id}', response_model=DeleteResponseSchema)
async def delete_service(service_id: int):
    res = await db_service.delete_service(service_id)
    return {'id': res}


@router.post('/status', response_model=StatusResponseSchema)
async def create_status(data: StatusSchema):
    res = await db_service.create_status(data.dict())

    return {
        'id': res.id,
        'name': res.name
    }


@router.get('/statuses', response_model=list[StatusResponseSchema])
async def get_statuses(user: User = Depends(current_user)):
    return await db_service.get_statuses()


@router.get('/status/{status_id}', response_model=StatusResponseSchema)
async def get_status_by_id(status_id: int):
    return await db_service.get_status_by_id(status_id)


@router.put('/status/{status_id}', response_model=StatusResponseSchema)
async def update_status(status_id: int, data: StatusSchema):
    res = await db_service.update_status(status_id, data.dict())

    return {'id': res.id, 'name': res.name}


@router.delete('/status/{status_id}', response_model=DeleteResponseSchema)
async def delete_status(status_id: int):
    res = await db_service.delete_status(status_id)

    return {'id': res}


@router.post('/order', response_model=OrderResponseSchema)
async def create_order(data: OrderSchema):
    res = await db_service.create_order(data.dict())

    return {
        'id': res.id,
        'status_id': res.status_id,
        'service_id': res.service_id,
        'user_id': res.user_id,
    }


@router.get('/orders', response_model=list[OrderResponseSchema])
async def get_orders(user: User = Depends(current_user)):
    return await db_service.get_orders()


@router.get('/order/{order_id}', response_model=OrderResponseSchema)
async def get_status_by_id(order_id: int):
    return await db_service.get_status_by_id(order_id)


@router.put('/order/{order_id}', response_model=OrderResponseSchema)
async def update_order(order_id: int, data: OrderSchema):
    res = await db_service.update_order(order_id, data.dict())

    return {
        'id': res.id,
        'status_id': res.status_id,
        'service_id': res.service_id,
        'user_id': res.user_id,
    }


@router.delete('/order/{order_id}', response_model=DeleteResponseSchema)
async def delete_order(order_id: int):
    res = await db_service.delete_order(order_id)

    return {'id': res}

