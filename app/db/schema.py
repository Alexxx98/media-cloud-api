from datetime import datetime

from sqlmodel import SQLModel


class CreateDirectory(SQLModel):
    name: str
    parent_id: int | None = None
    password: str | None = None
    uploaded_by: str | None = None


class DirectoryResponse(SQLModel):
    id: int
    type: str = 'directory'
    name: str
    parent_id: int | None = None
    added_by: str | None = None
    uploaded_at: datetime


class FileResponse(SQLModel):
    id: int
    type: str = 'media'
    name: str
    parent_id: int
    size: int
    mime_type: str
    added_by: str | None = None
    uploaded_at: datetime


class Rename(SQLModel):
    name: str


class ChangePassword(SQLModel):
    current_password: str | None = None
    new_password: str
