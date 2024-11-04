import bcrypt

from app.errors import NotValidPassword


def hash_pw(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def check_pw(password: str, hash: str) -> None:
    password_bytes = password.encode("utf-8")
    hash_bytes = hash.encode("utf-8")

    if not bcrypt.checkpw(password_bytes, hash_bytes):
        raise NotValidPassword
