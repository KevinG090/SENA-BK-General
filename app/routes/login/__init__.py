from fastapi import APIRouter
from psycopg.errors import Error as PGError

from db.queries.login import LoginQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ResponseBase,
)

router = APIRouter()


@router.get("/verify")
async def verify(email: str, passworld: str):
    """Metodo para validar que el correo"""

    try:
        results = await LoginQueries().login_usuario(email=email, passworld=passworld)
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
        raise Exception(f"{EnumErrors.ERROR_QUERY.value}: {exc_response}")
    except Exception as exc_response:
        raise Exception(f"{EnumErrors.ERROR_INESPERADO.value}: {exc_response}")

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
        raise Exception(f"{EnumErrors.ERROR_QUERY.value}: {exc_response}")
    except Exception as exc_response:
        raise Exception(f"{EnumErrors.ERROR_INESPERADO.value}: {exc_response}")

    return res
