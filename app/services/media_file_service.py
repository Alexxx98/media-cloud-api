import os

from fastapi import UploadFile, HTTPException, File
from sqlmodel import Session, select

from app.models.media_file import MediaFileModel


class MediaFileService:
    def __init__(self, session: Session):
        self._db = session

    # Get files by it's directory id
    def get_files(self, directory_id: int):
        return self._db.exec(select(MediaFileModel)).where(
            directory_id == MediaFileModel.directory_id
        )

    # Upload single file
    def upload_file(self, file: UploadFile = File(...)):
        if not file:
            return HTTPException(status_code=400, detail='No file provided')

        filename = file.filename
        destination = os.path.join(os.getenv('STORAGE_PATH'), filename)

        try:
            with open(destination, 'wb') as buffer:
                buffer.write(file.file.read())
        except Exception:
            return HTTPException(
                status_code=400, detail='Could not save the file'
            )

        return {'detail': file}
