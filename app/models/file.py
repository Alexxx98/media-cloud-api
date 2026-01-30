from datetime import datetime

from sqlmodel import SQLModel, Field


class FileModel(SQLModel, table=True):
    __tablename__ = 'file'

    id: int = Field(primary_key=True, index=True)
    type: str
    hashed_name: str | None = None
    original_name: str
    parent_id: int | None = Field(foreign_key='file.id')
    password_hash: bytes | None = None
    hash_salt: bytes | None = None
    size: int | None = None
    mime_type: str | None = None
    added_by: str | None = None
    added_at: datetime = Field(default_factory=datetime.now)
