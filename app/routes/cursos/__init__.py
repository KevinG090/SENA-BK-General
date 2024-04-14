""""""

from fastapi import APIRouter, Depends

from core.config import get_settings
from db.queries.cursos import CursosQueries

router = APIRouter()


@router.get("/listar-cursos")
async def get_list_courses():
    """"""
    return await CursosQueries().lista_paginada_cursos()


@router.post("/crear-cursos")
def create_course():
    """"""
    return [{"cursos": ""}]


@router.put("/modificar-cursos")
def edit_course():
    """"""
    return [{"cursos": ""}]
