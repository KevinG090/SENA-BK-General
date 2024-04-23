""" Modelos de eventos """

from schemas.responses_model.common import ModelConfig
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from schemas.utils import validate_type_number


class InputCreacionEvento(BaseModel):
    """"""

    fk_id_curso: Optional[str] = Field(default=None, examples=[1],max_length=10)
    nombre_evento: str = Field(..., examples=["Nombre evento"], max_length=20)
    contenido: str = Field(
        ...,
        examples=[
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua..."
        ],
        max_length=300,
    )

    @field_validator("fk_id_curso")
    @classmethod
    def validate_items(cls, v: Any):
        """"""
        new_val = validate_type_number(v)
        return v