from fastapi import APIRouter, UploadFile, Depends, Form, Header
from sqlmodel import Session

from app.services.media_cloud_service import MediaCloudService
from app.models.file import FileModel
from app.db.schema import (
    CreateDirectory,
    Rename,
    ChangePassword,
    DirectoryResponse,
    FileResponse
)
from app.db.session_dependency import get_session


router = APIRouter(prefix='/api/v1')


def get_media_file_service(session: Session = Depends(get_session)):
    return MediaCloudService(session=session)


# GET METHODS
# Get files and directories at the root
@router.get('/root', response_model=list[FileModel])
def get_root_files(service: MediaCloudService = Depends(
    get_media_file_service)
):
    return service.get_root_files()


# Get all files and directories of certain parent directory
@router.get('/directory/{parent_id}', response_model=list[FileModel])
def get_files(
    parent_id: int,
    x_directory_password: str | None = Header(default=None),
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.get_files(parent_id, x_directory_password)


# POST METHODS
# Create directory
@router.post('/directory/create', response_model=DirectoryResponse)
def create_directory(
    directory: CreateDirectory,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.create_directory(directory)


# Upload a file
@router.post('/file/upload', response_model=FileResponse)
def upload_file(
    file: UploadFile,
    parent_id: int = Form(...),
    mime_type: str = Form(...),
    uploaded_by: str | None = Form(None),
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.upload_file(
        file,
        parent_id,
        mime_type,
        uploaded_by
    )


# PATCH METHODS
# Rename directory
@router.patch(
        '/directory/{directory_id}/rename', response_model=DirectoryResponse
    )
def rename_directory(
    directory_id: int,
    data: Rename,
    x_directory_password: str | None = Header(default=None),
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.rename(directory_id, data, x_directory_password)


# Rename file
@router.patch('/file/{file_id}/rename', response_model=FileResponse)
def rename_file(
    file_id: int,
    data: Rename,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.rename(file_id, data)


# Change directory's password
@router.patch('/directory/{directory_id}/change_password')
def change_password(
    directory_id: int,
    data: ChangePassword,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.change_password(directory_id, data)


# DESTROY METHODS
# Delete directory
@router.delete('/directory/{directory_id}/delete')
def delete_directory(
    directory_id: int,
    x_directory_password: str | None = Header(default=None),
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.delete_directory(directory_id, x_directory_password)


# Delete file
@router.delete('/file/{file_id}/delete')
def delete_file(
    file_id: int,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.delete_file(file_id)
