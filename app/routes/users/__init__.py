""""""

from typing import Optional

from fastapi import APIRouter
from psycopg2.errors import DatabaseError
from psycopg2.errors import Error as PGError

from db.queries.users import UsersQueries
from schemas.responses_model.common import (
    DetailErrorObj,
    EnumErrors,
    EnumMsg,
    ErrorResponse,
    ExceptionResponse,
    ResponseBase,
)
from schemas.responses_model.users import (
    InputAsignacionUsuariosCursos,
    InputCreacionUsers,
    InputModificacionUsuario,
    InputEliminarAsignacionUsuariosCursos,
)

router = APIRouter()


@router.get("/listar-usuarios")
async def get_list_users(
    limit: int = 10,
    page: int = 1,
    pk_id_usuario: Optional[str] = None,
    nombre_usuario: Optional[str] = None,
    pk_id_curso: Optional[str] = None,
):
    """"""
    try:
        offset = (page - 1) * limit
        results = await UsersQueries().consultar_paginada_usuarios(
            limit,
            offset,
            pk_id_usuario,
            nombre_usuario,
            pk_id_curso,
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


@router.post("/crear-usuarios")
async def create_users(usuario: InputCreacionUsers):
    """Metodo para la creacion de usuarios"""

    try:
        results = await UsersQueries().crear_usuarios(usuario)

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


@router.put("/modificar-usuarios")
async def edit_users(pk_id_usuario: str, usuario: InputModificacionUsuario):
    """"""
    try:
        results_verify = await UsersQueries().verificar_usuarios(pk_id_usuario)
        if not results_verify.get("results", None):
            raise ErrorResponse(
                "No se encontro el usuario",
                error_status=404,
                error_obj=DetailErrorObj(
                    user_msg="No se encontro el usuario",
                    complete_info="Error al validar el usuario para poderlo modificar",
                ),
            )

        results_update = await UsersQueries().modificar_usuarios(pk_id_usuario, usuario)

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


@router.get("/consultar-usuario-especifico")
async def search_specify_user(pk_id_usuario: str):
    """"""
    try:
        results_verify = await UsersQueries().verificar_usuarios(pk_id_usuario)
        if not results_verify.get("results", None):
            raise ErrorResponse(
                "No se encontro el usuario",
                error_status=404,
                error_obj=DetailErrorObj(
                    user_msg="No se encontro el usuario",
                    complete_info="Error al validar el usuario para poderlo modificar",
                ),
            )
        res = ResponseBase(
            msg=f"{EnumMsg.CONSULTA.value} exitosa",
            codigo=str(200),
            status=True,
            obj=results_verify,
        )
    except ErrorResponse as exc_response:
        raise exc_response
    except (DatabaseError, PGError) as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise ExceptionResponse(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.post("/asignar-usuarios-cursos")
async def assign_users_courses(data: InputAsignacionUsuariosCursos):
    """"""
    try:
        results = await UsersQueries().asignar_curso_usuario(
            data.pk_id_usuario, data.pk_id_curso
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

@router.delete("/eliminar-relacion-usuarios-cursos")
async def delete_assign_users_courses(data: InputEliminarAsignacionUsuariosCursos):
    """"""
    try:
        results = await UsersQueries().eliminar_relacion_curso_usuario(
            data.fk_id_usuario, data.fk_id_curso
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
