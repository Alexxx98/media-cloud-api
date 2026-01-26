from fastapi import APIRouter, UploadFile, Depends, Form
from sqlmodel import Session

from app.services.media_cloud_service import MediaCloudService
from app.models.file import FileModel
from app.db.schema import CreateDirectory
from app.db.session_dependency import get_session


router = APIRouter(prefix='/api/v1')


def get_media_file_service(session: Session = Depends(get_session)):
    return MediaCloudService(session=session)


# GET METHODS
# Get files and directories at the root
@router.get('/directory', response_model=list[FileModel])
def get_root_files(service: MediaCloudService = Depends(
    get_media_file_service)
):
    return service.get_root_files()


# Get all files and directories of certain parent directory
@router.get('/directory/{parent_id}', response_model=list[FileModel])
def get_files(
    parent_id: int,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.get_files(parent_id)


# POST METHODS
# Create directory
@router.post('/directory/create', response_model=FileModel)
def create_directory(
    directory: CreateDirectory,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.create_directory(directory)


# Upload a file
@router.post('/upload', response_model=FileModel)
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


# DESTROY METHODS
# Delete file
@router.delete('/delete/{file_id}')
def delete_file(
    file_id: int,
    service: MediaCloudService = Depends(get_media_file_service)
):
    return service.delete_file(file_id)
