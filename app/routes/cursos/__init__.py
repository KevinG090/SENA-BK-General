""""""

from typing import Optional

from fastapi import APIRouter
from psycopg2.errors import DatabaseError, Error as PGError

from db.queries.cursos import CursosQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ResponseBase,
    ExceptionResponse
)
from schemas.responses_model.cursos import InputCreacionCurso, InputModificacionCurso

router = APIRouter()


@router.get("/listar-cursos")
async def get_list_courses(
    limit: int = 10,
    page: int = 1,
    pk_id_curso: Optional[str] = None,
    nombre_curso: Optional[str] = None,
):
    """Metodo para listar los cursos de manera paginada"""

    try:
        offset = (page - 1) * limit
        results = await CursosQueries().lista_paginada_cursos(
            limit, offset, pk_id_curso, nombre_curso
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


@router.post("/crear-cursos")
async def create_cursos(curso: InputCreacionCurso):
    """"""
    try:
        results = await CursosQueries().crear_cursos(curso)

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


@router.put("/modificar-cursos")
async def edit_course(pk_id_curso: str, curso: InputModificacionCurso):
    """"""
    try:
        results_verify = await CursosQueries().verificar_cursos(pk_id_curso)
        if not results_verify.get("results", None):
            raise ErrorResponse(
                "No se encontro el curso",
                error_status=404,
                error_obj=DetailErrorObj(
                    user_msg="No se encontro el curso",
                    complete_info="Error al validar el curso para poderlo modificar",
                ),
            )

        results_update = await CursosQueries().modificar_cursos(pk_id_curso, curso)

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
