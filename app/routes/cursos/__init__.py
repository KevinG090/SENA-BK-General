""""""

from typing import Optional

from fastapi import APIRouter
from psycopg.errors import Error as PGError

from db.queries.cursos import CursosQueries
from schemas.responses_model.common import EnumErrors, EnumMsg, ResponseBase
from schemas.responses_model.cursos import InputCreacionCurso

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
    except PGError as e:
        raise Exception(f"{EnumErrors.ERROR_QUERY.value}: {e}")
    except Exception as e:
        raise Exception(f"{EnumErrors.ERROR_INESPERADO.value}: {e}")

    return res


@router.post("/crear-cursos")
async def create_cursos(evento: InputCreacionCurso):
    """"""
    try:
        results = await CursosQueries().crear_cursos(evento)

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


@router.put("/modificar-cursos")
async def edit_course():
    """"""
    return [{"cursos": ""}]
