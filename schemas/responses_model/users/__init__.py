""" Modelos de eventos """

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from schemas.responses_model.common import ModelConfig, TipoUsuarios
from schemas.utils import validate_type_number


class InputCreacionUsers(BaseModel):
    """"""

    nombre_usuario: str = Field(..., examples=["nombre usuario"], max_length=50)
    celular: str = Field(..., examples=["3333333333"], max_length=12)
    correo: str = Field(..., examples=["example@gmail.com"], max_length=50)
    identificacion: str = Field(..., examples=["1234563216"], max_length=20)
    contraseña: str = Field(..., examples=["********"], max_length=50)
    fk_id_tipo_usuario: TipoUsuarios = Field(
        ..., examples=[TipoUsuarios.ESTUDIANTE.value]
    )

    @field_validator("identificacion")
    @classmethod
    def validate_items(cls, v: Any):
        """"""
        new_val = validate_type_number(v)
        return v

    @field_validator("fk_id_tipo_usuario", mode="after")
    @classmethod
    def change_return(cls, v: TipoUsuarios):
        """"""
        return int(v.value)


class InputModificacionUsuario(BaseModel):
    """"""

    nombre_usuario: Optional[str] = Field(
        default=None, examples=["nombre modificado"], max_length=50
    )
    celular: Optional[str] = Field(default=None, examples=["3444444444"], max_length=12)
    correo: Optional[str] = Field(
        default=None, examples=["exampleModificado@gmail.com"], max_length=50
    )
    identificacion: Optional[str] = Field(
        default=None, examples=["987654321"], max_length=20
    )
    contraseña: Optional[str] = Field(
        default=None, examples=["********2"], max_length=50
    )
    fk_id_tipo_usuario: Optional[TipoUsuarios] = Field(
        default=None, examples=[TipoUsuarios.ESTUDIANTE.value]
    )

    @field_validator("identificacion")
    @classmethod
    def validate_items(cls, v: Any):
        """"""
        new_val = validate_type_number(v)
        return v

    @field_validator("fk_id_tipo_usuario", mode="after")
    @classmethod
    def change_return(cls, v: TipoUsuarios):
        """"""
        return int(v.value)


class InputAsignacionUsuariosCursos(BaseModel):
    """"""

    pk_id_usuario: int = Field(..., examples=["5"])
    pk_id_curso: int = Field(..., examples=["6"])

class InputEliminarAsignacionUsuariosCursos(BaseModel):
    """"""

    fk_id_usuario: int = Field(..., examples=["5"])
    fk_id_curso: int = Field(..., examples=["6"])
