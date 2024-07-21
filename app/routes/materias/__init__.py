""""""

from typing import Optional

from fastapi import APIRouter
from psycopg2.errors import DatabaseError
from psycopg2.errors import Error as PGError

from db.queries.materias import MateriasQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ExceptionResponse,
    ResponseBase,
)
from schemas.responses_model.materias import (
    InputAsignacionMateriasCursos,
    InputCreacionMaterias,
    InputEliminarAsignacionMateriasCursos,
    InputModificacionMateria,
)

router = APIRouter()


@router.get("/listar-materias-cursos")
async def get_list_topics_courses(
    limit: int = 10,
    page: int = 1,
    pk_id_materia: Optional[str] = None,
    nombre_materia: Optional[str] = None,
    pk_id_curso: Optional[str] = None,
    nombre_curso: Optional[str] = None,
):
    """"""
    try:
        offset = (page - 1) * limit
        results = await MateriasQueries().lista_paginada_materias_cursos(
            limit,
            offset,
            pk_id_materia,
            nombre_materia,
            pk_id_curso,
            nombre_curso,
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
    except (DatabaseError, PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.post("/crear-materias")
async def create_topics(materia: InputCreacionMaterias):
    """"""
    try:
        results = await MateriasQueries().crear_materias(materia)

        res = ResponseBase(
            msg=f"{EnumMsg.CREACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except (DatabaseError, PGError) as e:
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
    except (DatabaseError, PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.post("/asignar-curso-materias")
async def assign_course_subjects(data: InputAsignacionMateriasCursos):
    """"""
    try:
        results = await MateriasQueries().asignar_curso_materias(
            data.pk_id_materia, data.pk_id_curso
        )

        res = ResponseBase(
            msg=f"{EnumMsg.ASIGNACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except (DatabaseError, PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.delete("/eliminar-relacion-curso-materias")
async def delete_assign_course_subjects(data: InputEliminarAsignacionMateriasCursos):
    """"""
    try:
        results = await MateriasQueries().eliminar_relacion_curso_materias(
            data.fk_id_materia, data.fk_id_curso
        )

        res = ResponseBase(
            msg=f"{EnumMsg.ELIMINACION.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results,
        )
    except (DatabaseError, PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res
