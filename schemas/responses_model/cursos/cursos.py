""" Modelos de eventos """

from schemas.responses_model.common import ModelConfig
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from schemas.utils import validate_type_number


class InputCreacionCurso(ModelConfig):
    """"""

    nombre_curso: str = Field(..., examples=["Nombre curso"], max_length=20)
