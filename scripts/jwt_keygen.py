import os
import shutil

import _base_script
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app.constants import JWT_FOLDER_PATH, JWT_PRIVATE_NAME, JWT_PUBLIC_NAME


if os.path.exists(JWT_FOLDER_PATH):
    shutil.rmtree(JWT_FOLDER_PATH)

os.mkdir(JWT_FOLDER_PATH)


def utf8(s: bytes):
    return str(s, "utf-8")


private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=4096, backend=default_backend()
)
public_key = private_key.public_key()


private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

with open(os.path.join(JWT_FOLDER_PATH, JWT_PRIVATE_NAME), "wb") as f:
    f.write(private_pem)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

with open(os.path.join(JWT_FOLDER_PATH, JWT_PUBLIC_NAME), "wb") as f:
    f.write(public_pem)
