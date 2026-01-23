from fastapi import FastAPI

from app.api.v1 import media_directory, media_file
from app.core.logging import setup_logging


setup_logging()


app = FastAPI()

app.include_router(media_directory.router)
app.include_router(media_file.router)
