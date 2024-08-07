from fastapi import APIRouter
from psycopg2.errors import DatabaseError
from psycopg2.errors import Error as PGError

from db.queries.login import LoginQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ExceptionResponse,
    ResponseBase,
)
from schemas.responses_model.login import InputLogin

router = APIRouter()


@router.post("/verify")
async def verify(input: InputLogin):
    """Metodo para el login"""

    try:
        results = await LoginQueries().login_usuario(
            email=input.data.email, password=input.data.password
        )
        if not results:
            raise ErrorResponse(
                "No se encontro el usuario",
                error_status=404,
                error_obj=DetailErrorObj(user_msg="No se encontro el usuario"),
            )
        res = ResponseBase(
            msg=f"{EnumMsg.CONSULTA.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except ErrorResponse as exc_response:
        raise exc_response
    except PGError as exc_response:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {exc_response}")
    except Exception as exc_response:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {exc_response}")

    return res


@router.get("/user")
async def buscar_info_user(pk_id_usuario: int):
    """Metodo para validar que el correo"""

    try:
        results = await LoginQueries().buscar_usuario(pk_id_usuario)
        if not results:
            raise ErrorResponse(
                "No se encontro el usuario",
                error_status=404,
                error_obj=DetailErrorObj(user_msg="No se encontro el usuario"),
            )
        res = ResponseBase(
            msg=f"{EnumMsg.CONSULTA.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except ErrorResponse as exc_response:
        raise exc_response
    except PGError as exc_response:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {exc_response}")
    except Exception as exc_response:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {exc_response}")

    return res
