""" Functions for use AES encyption """

import hashlib
import base64
from abc import ABC, abstractmethod

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Cipher(ABC):
    """Cipher interface"""

    @abstractmethod
    def encrypt(self, raw_data: str) -> bytes:
        """Function for encrypt an ``str`` data"""

    @abstractmethod
    def decrypt(self, enc_data: str) -> str:
        """Function for decrypt an encrypted data"""


class AESCipher(Cipher):
    """Class that implements AES Cipher"""

    def __init__(self, key: str, i_vec: str):
        self._key = base64.b64decode(key)
        self._i_vec = i_vec.encode("utf-8")
        self._cipher = AES.new(self._key, AES.MODE_CBC, self._i_vec)

    def encrypt(self, raw_data: str):
        return base64.b64encode(
            self._cipher.encrypt(
                pad(
                    raw_data.encode("utf-8"),
                    AES.block_size,
                )
            )
        )

    def decrypt(self, enc_data: str) -> str:
        return unpad(
            self._cipher.decrypt(base64.b64decode(enc_data)), AES.block_size
        ).decode("utf-8")
