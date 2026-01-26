from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Config(BaseSettings):
    class Config:
        env_file = 'db.env'

    app_name: str = 'MediaCloudAPI'
    debug: bool = False
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    @property
    def db_url(self):
        return f'postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:5434/{self.postgres_db}'


config = Config()
