from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.services.media_cloud_service import MediaCloudService
from app.models.file import FileModel
from app.db.session_dependency import get_session


router = APIRouter(prefix='/api/v1')


def get_media_file_service(session: Session = Depends(get_session)):
    return MediaCloudService(session=session)


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
