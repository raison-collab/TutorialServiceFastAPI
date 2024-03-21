from fastapi_users import schemas


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
