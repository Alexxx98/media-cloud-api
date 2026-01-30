import magic

from fastapi import UploadFile


class MediaUtils:
    async def detect_mime_type(file: UploadFile) -> str:
        header = await file.read(4096)
        await file.seek(0)
        return magic.from_buffer(header, mime=True)
