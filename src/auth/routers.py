from fastapi import APIRouter, Depends

from loader import fastapi_users
from src.auth.database import User
from src.auth.db_service import DBService
from src.auth.schemas import RoleCreate

router = APIRouter(
    prefix='/api',
    tags=['Main Api']
)

current_user = fastapi_users.current_user()
db_service = DBService()


@router.post('/role')
async def create_role(role: RoleCreate, user: User = Depends(current_user)):
    await db_service.create_role(role.dict())


@router.get('/role/{role_id}')
async def get_role(role_id: int, user: User = Depends(current_user)):
    return await db_service.get_role_by_id(role_id)


@router.get('/roles')
async def get_roles(user: User = Depends(current_user)):
    return await db_service.get_roles()


@router.delete('/role/{role_id}')
async def delete_role(role_id: int, user: User = Depends(current_user)):
    await db_service.delete_role(role_id)
