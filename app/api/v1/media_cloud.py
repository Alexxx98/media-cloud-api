from typing import Union

from fastapi import APIRouter, UploadFile, Query, Depends, Form, Header, Body
from sqlmodel import Session

from app.services.media_cloud_service import MediaCloudService
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
@router.get('/root', response_model=list[DirectoryResponse])
def get_root_files(service: MediaCloudService = Depends(
    get_media_file_service)
):
    return service.get_root_files()


# Get all files and directories of certain parent directory
@router.get(
    '/directory/{parent_id}',
    response_model=list[Union[DirectoryResponse, FileResponse]],

)
def get_files(
    parent_id: int,
    x_directory_password: str | None = Header(default=None),
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.get_files(parent_id, x_directory_password)


@router.get('/file/{file_id}/download')
async def download_file(
    file_id: int,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return await service.download_file(file_id)


@router.get('/file/{file_id}/stream')
async def stream_file(
    file_id: int,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return await service.stream_file(file_id)


# POST METHODS
# Create directory
@router.post('/directory/create', response_model=DirectoryResponse)
def create_directory(
    directory: CreateDirectory,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.create_directory(directory)


# Upload a files
@router.post('/file/upload', response_model=list[FileResponse])
async def upload_files(
    file: list[UploadFile],
    parent_id: int = Form(...),
    uploaded_by: str | None = Form(None),
    service: MediaCloudService = Depends(get_media_file_service)
):
    return await service.upload_files(
        file,
        parent_id,
        uploaded_by
    )


# Download files
@router.post('/files/download')
async def download_files(
    file_ids: list[int] = Query(...),
    request = Body(default=None),
    service: MediaCloudService = Depends(get_media_file_service)

):
    return await service.download_files(file_ids, request)


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


# Delete multiple files
@router.delete('/files/delete')
def delete_multiple_files(
    file_ids: list[int] = Query(...),
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.delete_multiple_files(file_ids)
