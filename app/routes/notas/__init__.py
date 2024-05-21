from typing import Optional

from fastapi import APIRouter
from psycopg2.errors import DatabaseError, Error as PGError
from db.queries.notas import NotasQueries
from schemas.responses_model.notas import InputCreacionNota, InputModificacionNota
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
            limit=limit,
            offset=offset,
            pk_id_materia=pk_id_materia,
            nombre_materia=nombre_materia,
            pk_id_curso=pk_id_curso,
            nombre_curso=nombre_curso,
            pk_id_usuario=pk_id_usuario,
        )
        res = ResponseBase(
            msg=f"{EnumMsg.CONSULTA_PAGINADA.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except (DatabaseError, PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.post("/crear-notas")
async def create_notas(nota: InputCreacionNota):
    """"""
    try:
        results_verify = await NotasQueries().verificar_config_estudiante(
            nota.fk_relacion_usuario_curso,
            nota.fk_relacion_curso_materia,
        )
        if not results_verify.get("results", None):
            msg = (
                "Error al verificar la configuracion del usuario,"
                "validar que el estudiante tenga asignado un curso y materia"
            )
            raise ErrorResponse(
                msg,
                error_status=500,
                error_obj=DetailErrorObj(
                    user_msg=msg,
                    complete_info="Error al validar la materia para poderlo modificar",
                ),
            )

        results = await NotasQueries().crear_notas(nota)

        res = ResponseBase(
            msg=f"{EnumMsg.CREACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except ErrorResponse as exc_response:
        raise exc_response
    except (DatabaseError, PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res
