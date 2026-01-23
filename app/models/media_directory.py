from datetime import datetime

from sqlmodel import SQLModel, Field


class MediaDirectoryModel(SQLModel, table=True):
    __tablename__ = 'media_directory'

    id: int = Field(primary_key=True)
    name: str
    parent_id: int | None = Field(
        default=None, foreign_key='media_directory.id'
    )
    password: str | None = None
    created_by: str | None = None
    created_at: datetime = Field(default_factory=datetime.now())
