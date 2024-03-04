from fastapi import FastAPI

from main_service.routers import router as main_router

app = FastAPI(
    title="Tutoring Service"
)

app.include_router(main_router)
