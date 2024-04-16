""""""

from fastapi import APIRouter
from psycopg2.errors import Error as PGError

from db.queries.cursos import CursosQueries
from schemas.responses_model.common import EnumErrors

router = APIRouter()


@router.get("/listar-cursos")
async def get_list_courses():
    """Metodo para listar los cursos de manera paginada"""

    try:
        res = await CursosQueries().lista_paginada_cursos()
    except PGError as e:
        raise Exception(f"{EnumErrors.ERROR_QUERY}: {e}")
    except Exception as e:
        raise Exception(f"{EnumErrors.ERROR_INESPERADO}: {e}")

    return res


@router.post("/crear-cursos")
def create_course():
    """"""
    return [{"cursos": ""}]


@router.put("/modificar-cursos")
def edit_course():
    """"""
    return [{"cursos": ""}]
