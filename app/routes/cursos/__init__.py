""""""

from fastapi import APIRouter
from psycopg.errors import Error as PGError

from db.queries.cursos import CursosQueries
from schemas.responses_model.common import (
    CreateResponse,
    EnumErrors,
    EnumMsg,
    ResponseBase,
)

router = APIRouter()


@router.get("/listar-cursos")
async def get_list_courses():
    """Metodo para listar los cursos de manera paginada"""

    try:
        results = await CursosQueries().lista_paginada_cursos()

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
async def create_course():
    """"""
    return [{"cursos": ""}]


@router.put("/modificar-cursos")
async def edit_course():
    """"""
    return [{"cursos": ""}]
