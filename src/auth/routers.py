from fastapi import APIRouter, Depends

from loader import fastapi_users
from src.auth.database import User, Role
from src.auth.db_service import DBService
from src.auth.schemas import RoleCreate, RoleResponseSchema, UserServiceDataResponseSchema, ResponseDeleteSchema

router = APIRouter(
    prefix='/api',
    tags=['Main Api']
)

current_user = fastapi_users.current_user()
db_service = DBService()


@router.post('/role', response_model=RoleResponseSchema)
async def create_role(role: RoleCreate, user: User = Depends(current_user)):
    role: Role = await db_service.create_role(role.dict())
    return {'id': role.id, 'name': role.name}


@router.get('/role/{role_id}', response_model=RoleResponseSchema)
async def get_role(role_id: int, user: User = Depends(current_user)):
    return await db_service.get_role_by_id(role_id)


@router.get('/roles', response_model=list[RoleResponseSchema])
async def get_roles(user: User = Depends(current_user)):
    return await db_service.get_roles()


@router.delete('/role/{role_id}', response_model=ResponseDeleteSchema)
async def delete_role(role_id: int, user: User = Depends(current_user)):
    await db_service.delete_role(role_id)
    return {'id': role_id}


@router.get("/user/service-data/{user_id}", response_model=UserServiceDataResponseSchema)
async def get_user_service_data(user_id: int, user: User = Depends(current_user)):
    return await db_service.get_user_service_data(user_id)
