""" Modelos de Login """
import json
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from core.config import get_settings
from schemas.utils.crypto import AESCipher


class InputDataLogin(BaseModel):
    """"""

    email: str = Field(..., examples=["example@gmail.com"])
    password: str = Field(..., example=["123456789"])


class InputLogin(BaseModel):
    """"""

    data: InputDataLogin

    @field_validator("data", mode="before")
    def capture_data(cls, v: Any):
        try:
            cipher = AESCipher(
                get_settings().APP_LLAVE_AES_ENCRYPT,
                get_settings().APP_IV_AES_ENCRYPT,
            )
            return json.loads(cipher.decrypt(json.dumps(str(v))))
        except Exception as ex:
            raise ValueError("Error al descifrar la informacion del usuario")
