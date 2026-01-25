from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.app_logging import setup_logging
from app.api.v1 import media_cloud
from app.db.session_dependency import engine


setup_logging()
SQLModel.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(media_cloud.router)
