import os

from fastapi import UploadFile, HTTPException, File
from sqlmodel import Session, select

from app.models.file import FileModel
from app.db.schema import CreateFile


class MediaCloudService:
    def __init__(self, session: Session):
        self._db = session

    def get_root_files(self):
        return self._db.exec(select(FileModel).where(
                FileModel.parent_id == None
            )
        ).all()

    def create_directory(self, directory: CreateFile):
        db_directory = FileModel(
            name=directory.name,
            file_type=directory.file_type,
            parent_id=directory.parent_id,
            size=directory.size,
            mime_type=directory.mime_type,
            uploaded_by=directory.uploaded_by
        )

        self._db.add(db_directory)
        self._db.commit()
        self._db.refresh(db_directory)
        return db_directory

    # Get files and directories by it's parent directory id
    def get_files(self, directory_id: int):
        return self._db.exec(select(FileModel).where(
            directory_id == FileModel.parent_id
        )).all()

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
