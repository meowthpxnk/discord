import base64
import hashlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class IDEncryptor:
    def __init__(self, key: str) -> None:
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt_id(self, id: int) -> str:
        id = str(id)
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.key), modes.CBC(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()

        padded_id = id.ljust(16)
        encrypted_id = (
            encryptor.update(padded_id.encode()) + encryptor.finalize()
        )

        return base64.b64encode(iv + encrypted_id).decode()

    def decrypt_id(self, encrypted_data: str) -> str:
        encrypted_data = base64.b64decode(encrypted_data.encode())

        iv = encrypted_data[:16]
        encrypted_id = encrypted_data[16:]

        cipher = Cipher(
            algorithms.AES(self.key), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_id = decryptor.update(encrypted_id) + decryptor.finalize()

        return decrypted_id.decode().strip()
