""" Modelos de notas """

from typing import Any, Optional

from pydantic import BaseModel, Field


class InputCreacionNota(BaseModel):
    """"""

    nota: float = Field(..., examples=["4"])
    observaciones: Optional[list] = Field(None, example=["Detalle de la nota"])
    fk_relacion_usuario_curso: int = Field(..., examples=["1"])
    fk_relacion_curso_materia: int = Field(..., examples=["2"])


class InputModificacionNota(BaseModel):
    """Modelo para la actualizacion de una nota"""

    nombre_curso: str = Field(..., examples=["Nombre modificado"], max_length=20)
