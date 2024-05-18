""""""

from typing import Optional

from fastapi import APIRouter
from psycopg2.errors import DatabaseError, Error as PGError

from db.queries.materias import MateriasQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ResponseBase,
    ExceptionResponse,
)
from schemas.responses_model.materias import (
    InputCreacionMaterias,
    InputModificacionMateria,
)

router = APIRouter()


@router.get("/listar-materias")
async def get_list_topics(
    limit: int = 10,
    page: int = 1,
    pk_id_materia: Optional[str] = None,
    nombre_materia: Optional[str] = None,
):
    """"""
    try:
        offset = (page - 1) * limit
        results = await MateriasQueries().lista_paginada_materias(
            limit,
            offset,
            pk_id_materia,
            nombre_materia,
        )
        res = ResponseBase(
            msg=f"{EnumMsg.CONSULTA_PAGINADA.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except (DatabaseError,PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.post("/crear-materias")
async def create_topics(evento: InputCreacionMaterias):
    """"""
    try:
        results = await MateriasQueries().crear_materias(evento)

        res = ResponseBase(
            msg=f"{EnumMsg.CREACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except (DatabaseError,PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.put("/modificar-materias")
async def edit_topics(pk_id_materia: str, materia: InputModificacionMateria):
    """"""
    try:
        results_verify = await MateriasQueries().verificar_materias(pk_id_materia)
        if not results_verify.get("results", None):
            raise ErrorResponse(
                "No se encontro la materia",
                error_status=404,
                error_obj=DetailErrorObj(
                    user_msg="No se encontro la materia",
                    complete_info="Error al validar la materia para poderlo modificar",
                ),
            )

        results_update = await MateriasQueries().modificar_materias(
            pk_id_materia, materia
        )

        res = ResponseBase(
            msg=f"{EnumMsg.MODIFICACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results_update,
        )
    except ErrorResponse as exc_response:
        raise exc_response
    except (DatabaseError,PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res
