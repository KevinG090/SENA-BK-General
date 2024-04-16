""""""

from enum import Enum

from pydantic import BaseModel, Field


class StatusService(BaseModel):
    """Model representing the service status."""

    service: str = Field(
        ..., example="Service ok!", description="Status of the service"
    )


class EnumErrors(Enum):
    """Modelo del msg de ``Errores estandarizados``\n

    VALORES PERMITIDOS\n

    ERROR_INESPERADO = "Exception"\n
    ERROR_QUERY = "Psycopg2Error"\n
    """

    ERROR_INESPERADO = "Exception"
    ERROR_QUERY = "Psycopg2Error"
