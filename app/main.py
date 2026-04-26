from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.routers import router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A FastAPI backend for the Kenya locations dataset, structured to support "
        "search and filtering patterns you can reuse in a book exchange app."
    ),
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(router)

