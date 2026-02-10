from datetime import datetime

from sqlmodel import SQLModel


class CreateDirectory(SQLModel):
    name: str
    parent_id: int | None = None
    password: str | None = None
    added_by: str | None = None


class DirectoryResponse(SQLModel):
    id: int
    type: str = 'directory'
    original_name: str
    parent_id: int | None = None
    added_by: str | None = None
    added_at: datetime


class FileResponse(SQLModel):
    id: int
    type: str = 'media'
    original_name: str
    parent_id: int
    size: int
    mime_type: str
    added_by: str | None = None
    added_at: datetime


class Rename(SQLModel):
    original_name: str


class ChangePassword(SQLModel):
    current_password: str | None = None
    new_password: str
