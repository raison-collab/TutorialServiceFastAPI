from fastapi import APIRouter

router = APIRouter(
    tags=['Main']
)


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
