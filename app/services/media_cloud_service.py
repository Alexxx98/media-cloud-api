import os

from pathlib import Path

from fastapi import HTTPException, UploadFile, File, Form
from sqlmodel import Session, select

from app.models.file import FileModel
from app.db.schema import CreateDirectory, RenameDirectory
from app.services.auth_service import AuthService


class MediaCloudService:
    def __init__(self, session: Session):
        self._db = session
        self.auth_service = AuthService(session)

    # GET METHODS
    # Get root directory
    def get_root_files(self):
        return self._db.exec(select(FileModel).where(
                FileModel.parent_id == None
            )
        ).all()

    # Get files and directories by it's parent directory id
    def get_files(self, directory_id: int):
        return self._db.exec(select(FileModel).where(
            directory_id == FileModel.parent_id
        )).all()

    # POST METHODS
    # Create directory
    def create_directory(self, directory: CreateDirectory):
        password = directory.password
        # Hash the password using bcrypt
        if password:
            password = self.auth_service.validate_password(password)

        db_directory = FileModel(
            name=directory.name,
            file_type=directory.file_type,
            parent_id=directory.parent_id,
            password=password,
            uploaded_by=directory.uploaded_by
        )

        self._db.add(db_directory)
        self._db.commit()
        self._db.refresh(db_directory)
        return db_directory

    # Upload single file
    def upload_file(
            self,
            file: UploadFile = File(...),
            parent_id: int = Form(...),
            mime_type: str = Form(...),
            uploaded_by: str | None = Form(None)
    ):
        if not file:
            return HTTPException(status_code=400, detail='No file provided')

        destination = os.path.join(os.getenv('STORAGE_PATH'), file.filename)

        # Create db metadata
        db_file = FileModel(
            name=file.filename,
            file_type='media',
            parent_id=parent_id,
            size=file.size,
            mime_type=mime_type,
            storage_path=destination,
            uploaded_by=uploaded_by
        )

        # Upload file to server storage
        try:
            with open(destination, 'wb') as buffer:
                buffer.write(file.file.read())
        except Exception:
            return HTTPException(
                status_code=400, detail='Could not save the file'
            )

        # Save metadata to db
        self._db.add(db_file)
        self._db.commit()
        self._db.refresh(db_file)

        return db_file

    # UPDATE METHODS
    # Rename
    def rename_directory(self, directory_id: int, data: RenameDirectory):
        db_directory = self._db.get(FileModel, directory_id)
        if not db_directory:
            raise HTTPException(status_code=404, detail='Directory not found.')

        # Sets desired key/keys to null if value provided
        update_data = data.model_dump(exclude_unset=True)

        # Assigns new value/values to previously nullified keys
        for key, value in update_data.items():
            setattr(db_directory, key, value)

        # Add updated model to db
        self._db.add(db_directory)
        self._db.commit()
        self._db.refresh(db_directory)

        return db_directory

    # DESTROY METHODS
    # Delete file
    def delete_file(self, file_id: int):
        # Get file metadata from db
        db_file = self._db.get(FileModel, file_id)

        if not db_file:
            raise HTTPException(status_code=404, detail='File not found')

        # Get file from filesystem
        file_path = Path(db_file.storage_path)

        # Delete file from filesystem
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as ext:
            raise HTTPException(
                status_code=500,
                detail=f'Delete file from storage failed: {ext}'
            )

        # Delete file metadata from db
        self._db.delete(db_file)
        self._db.commit()

        return {'status': 'File deleted'}
