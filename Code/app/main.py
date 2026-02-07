from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router

from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.models import sql_models # noqa: F401

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "AI Summarizer Service is running"}

app.include_router(router, prefix=settings.API_V1_STR)
