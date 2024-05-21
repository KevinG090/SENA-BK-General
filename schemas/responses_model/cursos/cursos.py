""" Modelos de cursos """

from pydantic import BaseModel, Field


class InputCreacionCurso(BaseModel):
    """"""

    nombre_curso: str = Field(..., examples=["Nombre curso"], max_length=20)


class InputModificacionCurso(BaseModel):
    """Modelo para la actualizacion del curso"""

    nombre_curso: str = Field(..., examples=["Nombre modificado"], max_length=20)
