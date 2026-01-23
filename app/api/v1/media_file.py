from fastapi import APIRouter, Depends

from app.services.media_file_service import MediaFileService
from app.db.dependencies import get_session
from app.models.media_file import MediaFileModel


router = APIRouter(prefix='/api/v1')


def get_media_file_service():
    return MediaFileService(session=get_session())


@router.get('/directory/{directory_id}', response_model=list[MediaFileModel])
def get_media_files(
    directory_id: int, service: MediaFileService = Depends(
        get_media_file_service
    )
):
    return service.get_files(directory_id)


@router.post('/directory/{directory_id}/upload')
def upload_file(
    directory_id: int, service: MediaFileService = Depends(
        get_media_file_service
    )
):
    return
