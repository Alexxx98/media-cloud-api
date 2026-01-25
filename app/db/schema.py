from enum import Enum

from sqlmodel import SQLModel


class FileType(str, Enum):
    FILE = 'media'
    DIRECTORY = 'directory'


class CreateFile(SQLModel):
    name: str
    file_type: FileType
    parent_id: int | None = None
    size: int | None = None
    mime_type: str | None = None
    storage_path: str | None = None
    uploaded_by: str | None = None
