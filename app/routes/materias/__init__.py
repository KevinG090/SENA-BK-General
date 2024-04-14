""""""

from fastapi import APIRouter, Depends

from core.config import get_settings

router = APIRouter()


@router.get("/listar-materias")
def get_list_topics():
    """"""
    return [{"materias": ""}]


@router.post("/crear-materias")
def create_topics():
    """"""
    return [{"materias": ""}]


@router.put("/modificar-materias")
def edit_topics():
    """"""
    return [{"materias": ""}]
