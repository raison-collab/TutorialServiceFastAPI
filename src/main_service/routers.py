from fastapi import APIRouter, Depends

from loader import fastapi_users
from src.auth.database import User
from .db_service import DBService
from .schemas import SubjectSchema

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

@router.post()


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