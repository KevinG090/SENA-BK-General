""""""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel, ConfigDict, Extra, Field

from .templates import error_msg_templates as error_msg
from .users import TipoUsuarios

AnyDict = Dict[str, Any]
ListedDict = List[AnyDict]


class StatusService(BaseModel):
    """Model representing the service status."""

    service: str = Field(
        ..., examples=["Service ok!"], description="Status of the service"
    )


class EnumErrors(Enum):
    """Modelo del msg de ``Errores estandarizados``\n

    VALORES PERMITIDOS\n

    ERROR_INESPERADO = "Exception"\n
    ERROR_QUERY = "Psycopg2Error"\n
    """

    ERROR_INESPERADO = "Exception"
    ERROR_QUERY = "Psycopg2Error"


class EnumMsg(Enum):
    """Modelo del msg de ``respuestas estandarizados``\n

    VALORES PERMITIDOS\n

    CONSULTA = "Consulta"\n
    CONSULTA_PAGINADA = "Consulta paginada"\n
    ELIMINACION = "Eliminacion"\n
    MODIFICACION = "Modificacion"\n
    CREACION = "Creacion"\n
    PETICION = "Peticion"\n
    """

    CONSULTA = "Consulta"
    CONSULTA_PAGINADA = "Consulta paginada"
    ELIMINACION = "Eliminacion"
    MODIFICACION = "Modificacion"
    CREACION = "Creacion"
    PETICION = "Peticion"


class ModelConfig(BaseModel):
    """New Model config with translated errors"""

    model_config = ConfigDict(extra="allow")


class DetailErrorObj(BaseModel):
    """Error Object Model"""

    complete_info: Any = ""
    user_msg: str = ""


class ResponseBase(BaseModel):
    """"""

    msg: str
    codigo: str
    status: bool
    obj: Any = {}


class CreateResponse(BaseException):
    def __init__(
        self,
        msg_res: EnumMsg,
        codigo_res: int,
        status_res: bool,
        obj_res: AnyDict,
    ):
        res = ResponseBase(
            msg=f"{msg_res.value} {'exitosa' if status_res else 'fallida'}",
            codigo=str(codigo_res),
            status=status_res,
            obj=obj_res,
        )

        return res


class ResponseBaseError(ResponseBase):
    """ """

    class ErrorObj(BaseModel):
        """ """

        error: List[DetailErrorObj]

    obj: ErrorObj
    status: bool = False


class ErrorResponse(Exception):
    """Custom exception"""

    _error_list = []
    error_msg: str
    error_status: int
    codigo_error: str

    def __init__(
        self,
        error_msg: str,
        error_status: int,
        error_obj: DetailErrorObj,
        codigo_error: str = "0",
    ) -> None:
        super().__init__(error_obj)
        self._error_list = [error_obj]

        self.error_msg = error_msg
        self.error_status = error_status
        self.codigo_error = codigo_error

    @property
    def args(self):
        """Override property for use the `ResponseBase`"""
        type_code = f"[{self.codigo_error}]" if self.codigo_error != "0" else ""

        res = ResponseBase(
            status=False,
            codigo=self.codigo_error,
            msg=f"Error respuesta: ({self.error_msg} {type_code})",
            obj={"error": [_error for _error in self._error_list]},
        )

        args: Tuple[ResponseBase, int] = (res, self.error_status)

        return args

    @property
    def error_list(self):
        """Dict with all errors acumulated per request"""
        return self._error_list
