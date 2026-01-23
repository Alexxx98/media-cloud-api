import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Config(BaseSettings):
    app_name: str = 'MediaCloudAPI'
    debug: bool = False
    db_name: str = os.getenv('POSTGRES_DB')
    db_user: str = os.getenv('POSTGRES_USER')
    db_password: str = os.getenv('POSTGRES_PASSWORD')

    @property
    def db_url(self):
        return f'postgresql+psycopg2://{self.db_user}:{self.db_password}\
    @db:5432/{self.db_name}'


config = Config()
