from enum import Enum

from sqlmodel import SQLModel


class FileType(str, Enum):
    FILE = 'media'
    DIRECTORY = 'directory'


class CreateDirectory(SQLModel):
    name: str
    parent_id: int | None = None
    password: str | None = None
    uploaded_by: str | None = None


class Rename(SQLModel):
    name: str


class ChangePassword(SQLModel):
    current_password: str | None = None
    new_password: str
