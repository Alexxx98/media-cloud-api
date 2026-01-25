from datetime import datetime

from sqlmodel import SQLModel, Field

from app.db.schema import FileType


class FileModel(SQLModel, table=True):
    __tablename__ = 'file'

    id: int = Field(primary_key=True, index=True)
    name: str
    file_type: FileType = Field(nullable=False)
    parent_id: int | None = Field(foreign_key='file.id')
    size: int | None = None
    mime_type: str | None = None
    storage_path: str | None = None
    uploaded_by: str | None = None
    uploaded_at: datetime = Field(default_factory=datetime.now)
