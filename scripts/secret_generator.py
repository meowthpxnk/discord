import base64
import os

import _base_script
from cryptography.fernet import Fernet


key = os.urandom(32)
print(f'Your secret key: "{base64.b64encode(key).decode()}"')
