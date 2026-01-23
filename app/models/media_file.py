from datetime import datetime

from sqlmodel import SQLModel, Field


class MediaFileModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    filename: str
    directory_id: int = Field(foreign_key='media_directory.id')
    size: int
    mime_type: str
    storage_path: str
    upload_by: str | None = None
    uploaded_at: datetime = Field(default_factory=datetime.now)
