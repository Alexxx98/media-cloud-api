import os

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.core.app_logging import setup_logging
from app.api.v1 import media_cloud
from app.db.session_dependency import engine


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(bind=engine)
    yield
    pass

app = FastAPI(lifespan=lifespan)

origins = os.getenv('ORIGINS')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(media_cloud.router)
