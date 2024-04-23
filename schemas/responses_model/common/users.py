""""""

from enum import Enum


class TipoUsuarios(Enum):
    """Modelo de ``Tipos de usuarios``\n

    VALORES PERMITIDOS\n

    ADMINISTRADOR = "3"\n
    PROFESOR = "2"\n
    ESTUDIANTE = "1"\n
    """

    ADMINISTRADOR = "3"
    PROFESOR = "2"
    ESTUDIANTE = "1"
