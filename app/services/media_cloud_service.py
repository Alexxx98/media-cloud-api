import io
import zipfile

from pathlib import Path

from fastapi import HTTPException, UploadFile, Form, Header
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel import Session, select

from app.core.constants import STORAGE_PATH
from app.models.file import FileModel
from app.db.schema import CreateDirectory, Rename, ChangePassword
from app.services.auth_service import AuthService
from app.utils.media_utils import MediaUtils


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
    def get_files(
        self,
        directory_id: int,
        x_directory_password: str | None = Header(default=None)
    ):
        directory = self._db.get(FileModel, directory_id)
        if directory.password_hash:
            self.auth_service.verify_access(
                directory, x_directory_password
            )

        return self._db.exec(select(FileModel).where(
            directory_id == FileModel.parent_id
        )).all()

    # Download file
    async def download_file(self, file_id: int):
        file = self._db.get(FileModel, file_id)
        file_path = STORAGE_PATH / file.hashed_name
        return FileResponse(
            file_path,
            headers={
                'Content-Disposition': f'attachment; filename={file.original_name}'
            }
        )
    
    # Download multiple files
    async def download_multiple_files(self, file_ids: list[int]):
        buffer = io.BytesIO()

        # Compress files binary to zip archive
        with zipfile.ZipFile(
            buffer, 'w', compression=zipfile.ZIP_DEFLATED
        ) as zip:
            # Find file path by each id
            for index, file_id in enumerate(file_ids):
                file = self._db.get(FileModel, file_id)
                file_path = STORAGE_PATH / file.hashed_name
                if not file_path:
                    continue

                # Write file to zip archive
                zip.write(file_path, arcname=file.original_name)

                # if last file, set archive name to parent directory name
                try:
                    file_ids[index + 1]
                except IndexError:
                    parent_dir = self._db.exec(
                        select(FileModel).where(FileModel.id == file.parent_id)
                    ).one()
                    arch_name = parent_dir.original_name

        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type='application/zip',
            headers={
                'Content-Disposition': f'attachment; filename={arch_name}.zip'
            },
            # Content-Disposition header informs how to process
            # response payload and additional info
        )

    # Download directory
    async def download_directory(self, directory_id: int):
        files = self._db.exec(
            select(FileModel).where(FileModel.parent_id == directory_id)
        ).all()

        def create_file_structure(file: FileModel):
            if file.type == 'directory':
                dir_files = self._db.exec(
                    select(FileModel).where(FileModel.parent_id == file.id)
                ).all()
                for dir_file in dir_files:
                    if dir_file.type == 'direcotry':
                        create_file_structure(dir_file)

            return

        for file in files:
            if file.type == 'directory':
                dir_files = self._db.exec(
                    select(FileModel).where(FileModel.parent_id == file.id)
                ).all()
        
        # TODO: Implement logic to download whole directory tree

        return

    # Stream file
    async def stream_file(self, file_id: int):
        file = self._db.get(FileModel, file_id)
        file_path = STORAGE_PATH / file.hashed_name
        return FileResponse(
            file_path,
            filename=file.original_name,
            headers={
                'Content-Disposition': 'inline;'
            }
        )

    # POST METHODS
    # Create directory
    def create_directory(self, directory: CreateDirectory):
        password = directory.password
        salt = None
        # Hash the password using bcrypt
        if password:
            password, salt = self.auth_service.create_password(password)

        db_directory = FileModel(
            type='directory',
            original_name=directory.original_name,
            parent_id=directory.parent_id,
            password_hash=password,
            hash_salt=salt,
            added_by=directory.uploaded_by
        )

        self._db.add(db_directory)
        self._db.commit()
        self._db.refresh(db_directory)
        return db_directory

    # Upload files
    async def upload_files(
        self,
        files: list[UploadFile],
        directory_id: int = Form(...),
        uploaded_by: str | None = Form(default=None)
    ) -> list[FileModel]:
        if not files:
            return HTTPException(status_code=400, detail='No Files provided')

        response_files = []

        for file in files:
            hashed_name = self.auth_service.create_password(file.filename)
            destination = STORAGE_PATH / hashed_name[0].decode('utf-8')
            mime_type = await MediaUtils.detect_mime_type(file)

            try:
                with open(destination, 'wb') as media_file:
                    media_file.write(file.file.read())
            except Exception:
                raise HTTPException(
                    status_code=400, detail='Failed to save the file.'
                )

            db_file = FileModel(
                type='media',
                hashed_name=hashed_name[0].decode('utf-8'),
                original_name=file.filename,
                parent_id=directory_id,
                size=file.size,
                mime_type=mime_type,
                added_by=uploaded_by
            )

            self._db.add(db_file)
            self._db.commit()
            self._db.refresh(db_file)

            response_files.append(db_file)

        return response_files

    # PATCH METHODS
    # Rename file or directory
    def rename(
        self,
        id: int,
        data: Rename,
        x_directory_password: str | None = Header(default=None)
    ):
        file = self._db.get(FileModel, id)
        if not file:
            raise HTTPException(status_code=404, detail='Directory not found.')

        # Validate password if directory
        if file.type == 'directory':
            if file.password_hash:
                self.auth_service.verify_access(file, x_directory_password)

        # Sets desired key/keys to null if value provided
        update_data = data.model_dump(exclude_unset=True)

        # Assigns new value/values to previously nullified keys
        for key, value in update_data.items():
            setattr(file, key, value)

        # Add updated model to db
        self._db.add(file)
        self._db.commit()
        self._db.refresh(file)

        return file

    # Change directory's password
    def change_password(self, directory_id, data: ChangePassword):
        directory = self._db.get(FileModel, directory_id)

        new_password, new_salt = self.auth_service.change_password(
            directory, data.current_password, data.new_password
        )

        directory.password_hash = new_password
        directory.hash_salt = new_salt

        self._db.add(directory)
        self._db.commit()
        self._db.refresh(directory)

        return {'status': 'Password successfully changed.'}

    # DESTROY METHODS
    # Delete directory with its content
    def delete_directory(
        self,
        directory_id: int,
        x_directory_password: str | None = Header(default=None)
    ):
        directory = self._db.get(FileModel, directory_id)
        if directory.password_hash:
            self.auth_service.verify_access(
                directory, x_directory_password
            )

        media_files = self._db.exec(
            select(FileModel).where(FileModel.parent_id == directory_id)
        ).all()

        # Remove files
        for file in media_files:
            # Remove recursively if directory
            if file.type == 'directory':
                self.delete_directory(file.id)

            # First remove file from filesystem
            if file.hashed_name:
                file_path = Path(STORAGE_PATH / file.hashed_name)

                try:
                    if file_path.exists():
                        file_path.unlink()
                except Exception as ext:
                    raise HTTPException(
                        status_code=500,
                        detail=f'Delete file from storage failed: {ext}'
                    )

            # Delete file metadata from db
            self._db.delete(file)
            self._db.commit()

        # Delete directory
        self._db.delete(directory)
        self._db.commit()

        return {'status': 'Directory successfully deleted.'}

    # Delete file
    def delete_file(self, file_id: int):
        # Get file metadata from db
        db_file = self._db.get(FileModel, file_id)

        if not db_file:
            raise HTTPException(status_code=404, detail='File not found')

        # Get file from filesystem
        file_path = Path(STORAGE_PATH / db_file.hashed_name)

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

    # Delete multiple files
    def delete_multiple_files(self, files_id: list[int]):
        for file_id in files_id:
            file_data = self._db.get(FileModel, file_id)
            file_path = Path(STORAGE_PATH / file_data.hashed_name)

            # Remove file from filesystem
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception as ext:
                raise HTTPException(
                    status_code=500,
                    detail=f'Deleting file failed: {ext}'
                )

            # Remove from db
            self._db.delete(file_data)
            self._db.commit()

        return {'status': 'files deleted.'}
