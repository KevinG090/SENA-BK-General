from typing import Optional

from fastapi import APIRouter
from psycopg2.errors import DatabaseError, Error as PGError
from db.queries.notas import NotasQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ResponseBase,
    ExceptionResponse,
)
router = APIRouter()

@router.get("/listar-notas")
async def get_list_notas(
    limit: int = 10,
    page: int = 1,
    pk_id_materia: Optional[str] = None,
    nombre_materia: Optional[str] = None,
    pk_id_curso: Optional[str] = None,
    nombre_curso: Optional[str] = None,
    pk_id_usuario: Optional[str] = None,
):
    """"""
    try:
        offset = (page - 1) * limit
        results = await NotasQueries().lista_paginada_notas(
            limit = limit,
            offset = offset,
            pk_id_materia = pk_id_materia,
            nombre_materia = nombre_materia,
            pk_id_curso = pk_id_curso,
            nombre_curso = nombre_curso,
            pk_id_usuario = pk_id_usuario
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