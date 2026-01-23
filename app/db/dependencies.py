from sqlmodel import Session, create_engine

from app.core.config import config


engine = create_engine(config.db_url)


def get_session():
    with Session(engine) as session:
        yield session
