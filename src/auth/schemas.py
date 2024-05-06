from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    first_name: str
    second_name: str
    last_name: str
    card_number: str
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    second_name: str
    last_name: str
    card_number: str
    role_id: int


class RoleCreate(BaseModel):
    name: str


class RoleResponseSchema(RoleCreate):
    id: int


class UserServiceDataResponseSchema(BaseModel):
    user_id: int
    role_id: int
    f_name: str
    s_name: str
    l_name: str


class ResponseDeleteSchema(BaseModel):
    id: int
