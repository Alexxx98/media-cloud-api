from enum import Enum

from sqlmodel import SQLModel


class FileType(str, Enum):
    FILE = 'media'
    DIRECTORY = 'directory'


class CreateDirectory(SQLModel):
    name: str
    file_type: FileType = 'directory'
    parent_id: int | None = None
    password: bytes | None = None
    uploaded_by: str | None = None


class RenameDirectory(SQLModel):
    name: str


class ChangePassword(SQLModel):
    password: str
