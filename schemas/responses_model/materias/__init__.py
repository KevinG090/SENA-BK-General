""" Modelos de eventos """

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from schemas.responses_model.common import ModelConfig
from schemas.utils import validate_type_number


class InputCreacionMaterias(BaseModel):
    """"""

    nombre_materia: str = Field(..., examples=["Nombre materia"], max_length=20)
    descripcion: Optional[str] = Field(
        default=None,
        examples=["Lorem ipsum dolor sit amet, consectetur adipiscing elit..."],
        max_length=60,
    )


class InputModificacionMateria(BaseModel):
    """"""

    nombre_materia: Optional[str] = Field(examples=["Nombre modificado"], max_length=20)
    descripcion: Optional[str] = Field(
        default=None,
        examples=["Lorem ipsum dolor sit amet, consectetur adipiscing elit..."],
        max_length=60,
    )


class InputAsignacionMateriasCursos(BaseModel):
    """"""

    pk_id_materia: int = Field(..., examples=["5"])
    pk_id_curso: int = Field(..., examples=["6"])

class InputEliminarAsignacionMateriasCursos(BaseModel):
    """"""

    fk_id_materia: int = Field(..., examples=["5"])
    fk_id_curso: int = Field(..., examples=["6"])
