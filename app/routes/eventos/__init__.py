""""""

from typing import Optional

from fastapi import APIRouter
from psycopg.errors import Error as PGError

from db.queries.eventos import EventosQueries
from schemas.responses_model.common import (
    EnumErrors,
    EnumMsg,
    ResponseBase,
)
from schemas.responses_model.eventos import (
    InputCreacionEvento,
)

router = APIRouter()

@router.get("/listar-eventos")
async def get_list_events(
    limit: int = 10,
    page: int = 1,
    fk_id_curso: Optional[str] = None,
    nombre_evento: Optional[str] = None,
):
    """Metodo para listar los cursos de manera paginada"""

    try:
        offset = (page - 1) * limit
        results = await EventosQueries().lista_paginada_eventos(
            limit, offset, fk_id_curso, nombre_evento
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
async def edit_events():
    """"""
    return [{"eventos": ""}]