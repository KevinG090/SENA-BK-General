""""""

from typing import Optional

from fastapi import APIRouter
from psycopg.errors import Error as PGError

from db.queries.eventos import EventosQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ResponseBase,
)
from schemas.responses_model.eventos import (
    InputCreacionEvento,
    InputModificacionEventos,
)

router = APIRouter()


@router.get("/listar-eventos")
async def get_list_events(
    limit: int = 10,
    page: int = 1,
    fk_id_curso: Optional[str] = None,
    nombre_evento: Optional[str] = None,
    pk_id_evento: Optional[str] = None,
):
    """Metodo para listar los cursos de manera paginada"""

    try:
        offset = (page - 1) * limit
        results = await EventosQueries().lista_paginada_eventos(
            limit, offset, fk_id_curso, nombre_evento, pk_id_evento
        )

        res = ResponseBase(
            msg=f"{EnumMsg.CONSULTA_PAGINADA.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except PGError as e:
        raise Exception(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise Exception(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.post("/crear-eventos")
async def create_events(evento: InputCreacionEvento):
    """"""
    try:
        results = await EventosQueries().crear_eventos(evento)

        res = ResponseBase(
            msg=f"{EnumMsg.CREACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except PGError as e:
        raise Exception(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise Exception(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.put("/modificar-eventos")
async def edit_events(pk_id_evento: str, evento: InputModificacionEventos):
    """"""
    try:
        results_verify = await EventosQueries().verificar_eventos(pk_id_evento)
        if not results_verify.get("results", None):
            raise ErrorResponse(
                "No se encontro el evento",
                error_status=404,
                error_obj=DetailErrorObj(
                    user_msg="No se encontro el evento",
                    complete_info="Error al validar el evento para poderlo modificar",
                ),
            )

        results_update = await EventosQueries().modificar_eventos(pk_id_evento, evento)

        res = ResponseBase(
            msg=f"{EnumMsg.MODIFICACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results_update,
        )
    except ErrorResponse as exc_response:
        raise exc_response
    except PGError as e:
        raise Exception(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise Exception(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res
