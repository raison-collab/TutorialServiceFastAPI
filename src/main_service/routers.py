from fastapi import APIRouter, Depends

from loader import fastapi_users
from src.auth.database import User

router = APIRouter(
    tags=['Main']
)

current_user = fastapi_users.current_user()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/protected")
async def protected(user: User = Depends(current_user)):
    return {"message": f"Hello {user.email}"}
