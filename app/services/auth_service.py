import bcrypt

from fastapi import HTTPException
from sqlmodel import Session

from app.models.file import FileModel


class AuthService():
    def __init__(self, session: Session):
        self._db = session

    def create_password(self, password: str) -> tuple[bytes]:
        """ Create a new password hash """
        # First turn it into the array of bytes
        password_bytes = password.encode('utf-8')

        # generate the salt
        salt = bcrypt.gensalt()

        # Finally hash the password
        password_hash = bcrypt.hashpw(password_bytes, salt)

        return (password_hash, salt)

    def hash_password(self, password: str, salt: bytes) -> bytes:
        """ Hash the password with already existing salt """
        password_bytes = password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, salt)
        return password_hash

    def change_password(
            self, directory: FileModel, current_password, new_password
    ) -> tuple[bytes]:
        # Validate current password if exists
        if directory.password_hash:
            if not self.validate_password(directory, current_password):
                raise HTTPException(
                    status_code=403, detail='Current password does not match.'
                )

        password_hash, salt = self.create_password(new_password)
        return (password_hash, salt)

    def validate_password(self, directory: FileModel, password: str) -> bool:
        password_hash = self.hash_password(password, directory.hash_salt)
        if password_hash == directory.password_hash:
            return True
        return False

    def verify_access(
            self,
            directory: FileModel,
            password: str
    ):
        if not password:
            raise HTTPException(status_code=401, detail='Password required.')

        if not self.validate_password(directory, password):
            raise HTTPException(status_code=401, detail='Invalid password.')
