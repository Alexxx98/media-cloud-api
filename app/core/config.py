from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Config(BaseSettings):
    class Config:
        env_file = 'db.env'

    app_name: str = 'MediaCloudAPI'
    debug: bool = False
    db_name: str
    db_user: str
    db_password: str
    db_host: str

    @property
    def db_url(self):
        return f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:5434/{self.db_name}'


config = Config()
