from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str


class UserCreate(schemas.BaseUserCreate):
    email: str
