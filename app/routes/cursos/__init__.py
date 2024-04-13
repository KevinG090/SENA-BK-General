""""""

from fastapi import APIRouter, Depends
from core.config import get_settings

router = APIRouter()


@router.get("/listar-cursos")
def get_list_courses():
    """"""
    return [{"cursos":""}]

@router.post("/crear-cursos")
def create_course():
    """"""
    return [{"cursos":""}]

@router.put("/modificar-cursos")
def edit_course():
    """"""
    return [{"cursos":""}]