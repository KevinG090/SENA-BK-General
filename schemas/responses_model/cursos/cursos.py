""" Modelos de eventos """

from pydantic import BaseModel, Field


class InputCreacionCurso(BaseModel):
    """"""

    nombre_curso: str = Field(..., examples=["Nombre curso"], max_length=20)
