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
