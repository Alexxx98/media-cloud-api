import bcrypt

from fastapi import HTTPException
from sqlmodel import Session

from app.models.file import FileModel


class AuthService():
    def __init__(self, session: Session):
        self._db = session

    def hash_password(self, password: str) -> bytes:
        # First turn it into the array of bytes
        password_bytes = password.encode('utf-8')

        # generate the salt
        salt = bcrypt.gensalt()

        # Finally hash the password
        password_hash = bcrypt.hashpw(password_bytes, salt)

        return password_hash

    def change_password(
            self, directory: FileModel, current_password, new_password
    ) -> bytes:
        # Validate current password if exists
        if directory.password:
            if not self.validate_password(directory, current_password):
                raise HTTPException(
                    status_code=403, detail='Current password does not match.'
                )

        password_hash = self.hash_password(new_password)
        return password_hash

    def validate_password(self, directory: FileModel, password: str) -> bool:
        password_hash = self.hash_password(password)
        print(password_hash)
        print(directory.password)
        if password_hash == directory.password:
            return True
        return False
