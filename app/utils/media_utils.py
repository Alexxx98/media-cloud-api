import os
import magic

from fastapi import UploadFile


class MediaUtils:
    async def detect_mime_type(file: UploadFile) -> str:
        header = await file.read(4096)
        await file.seek(0)
        return magic.from_buffer(header, mime=True)

    def make_file_path(filename: str, index: int) -> str:
        storage_path = os.getenv('STORAGE_PATH')
        file_path: str = os.path.join(storage_path, filename)
        while os.path.exists(file_path):
            file_path = os.path.join(storage_path, f'({index}){filename}')
            index += 1
        return file_path
