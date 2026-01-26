import bcrypt

from sqlmodel import Session


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
            self, directory_id, current_password, new_password
    ) -> bytes:
        # TODO: Implement password changing logic
        return

    def validate_password(self, directory_id, password: str) -> bool:
        # TODO: Implement password validation logic
        return
