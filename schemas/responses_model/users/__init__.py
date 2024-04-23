""" Modelos de eventos """

from schemas.responses_model.common import ModelConfig, TipoUsuarios
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from schemas.utils import validate_type_number


class InputCreacionUsers(BaseModel):
    """"""

    nombre_usuario: str = Field(..., examples=["nombre usuario"],max_length=50)
    celular: str = Field(..., examples=["3333333333"], max_length=12)
    correo: str = Field(..., examples=["example@gmail.com"],max_length=50)
    identificacion: str = Field(..., examples=["1234563216"], max_length=20)
    contraseña: str = Field(..., examples=["********"],max_length=50)
    fk_id_tipo_usuario: TipoUsuarios = Field(..., examples=[TipoUsuarios.ESTUDIANTE.value])

    @field_validator("identificacion")
    @classmethod
    def validate_items(cls, v: Any):
        """"""
        new_val = validate_type_number(v)
        return v

    @field_validator("fk_id_tipo_usuario",mode="after")
    @classmethod
    def change_return(cls, v: TipoUsuarios):
        """"""
        return int(v.value)