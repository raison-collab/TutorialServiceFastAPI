from fastapi import APIRouter, Depends

from loader import fastapi_users
from src.auth.database import User
from .db_service import DBService
from .schemas import SubjectSchema, ServiceSchema, StatusSchema, OrderSchema

router = APIRouter(
    prefix='/api',
    tags=['Main Api']
)

current_user = fastapi_users.current_user()
db_service = DBService()


@router.post("/subject")
async def create_subject(data: SubjectSchema):
    res = await db_service.create_subject(data.dict())

    return {"id": res}


@router.get("/subjects")
async def get_subjects():
    res = await db_service.get_subjects()

    return {"data": res}


@router.get("/subject/{subject_id}")
async def get_subject_by_id(subject_id: int):
    res = await db_service.get_subject_by_id(subject_id)

    return res


@router.put("/subject/{subject_id}")
async def update_subject(subject_id: int, data: SubjectSchema):
    res = await db_service.update_subject(subject_id, data.dict())

    return {"id": res}


@router.delete("/subject/{subject_id}")
async def delete_subject(subject_id: int):
    res = await db_service.delete_subject(subject_id)

    return {"id": res}

@router.post('/service')
async def create_service(data: ServiceSchema):
    res = await db_service.create_service(data.dict())

    return {'id':res }

@router.get('/services')
async def get_services():
    res = await db_service.get_services()

    return {'data': res}

@router.get('/service/{service_id}')
async def get_service_by_id(service_id: int):
    res = await db_service.get_service_by_id(service_id)

    return res

@router.put('/service/{service_id}')
async def update_service(service_id: int, data: ServiceSchema):
    res = await db_service.update_service(service_id, data.dict())

    return {'id': res}

@router.delete('/service/{service_id}')
async def delete_service(service_id: int):
    res = await db_service.delete_service(service_id)

    return {'id': res}


@router.post('/status')
async def create_status(data: StatusSchema):
    res = await db_service.create_status(data.dict())

    return {'id': res}

@router.get('/statuses')
async def get_statuses():
    res = await db_service.get_statuses()

    return {'data': res}

@router.get('/status/{status_id}')
async def get_status_by_id(status_id: int):
    res = await db_service.get_status_by_id(status_id)

    return res

@router.put('/status/{status_id}')
async def update_status(status_id: int, data: StatusSchema):
    res = await db_service.update_status(status_id, data.dict())

    return {'id': res}

@router.delete('/status/{status_id}')
async def delete_status(status_id: int):
    res = await db_service.delete_status(status_id)

    return {'id': res}

@router.post('/order')
async def create_order(data: OrderSchema):
    res = await db_service.create_service(data.dict())

    return {'id': res}

@router.get('/orders')
async def get_orders():
    res = await db_service.get_orders()

    return {'data': res}

@router.get('/order/{order_id}')
async def get_status_by_id(order_id: int):
    res = await db_service.get_status_by_id(order_id)

    return {'id': res}

@router.put('/order/{order_id}')
async def update_order(order_id: int, data: OrderSchema):
    res = await db_service.update_order(order_id,data.dict())

    return {'id': res}

@router.delete('/order/{order_id}')
async def delete_order(order_id: int):
    res = await db_service.delete_order(order_id)

    return {'id': res}



@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/name")
async def name(name_: str):
    return {"name": f"{name_}"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/protected")
async def protected(user: User = Depends(current_user)):
    return {"message": f"Hello {user.email}"}


@router.get("/age")
async def age_(age: int):
    return {"message": age}