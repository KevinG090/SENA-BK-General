""""""

from fastapi import APIRouter, Depends

from core.config import get_settings

router = APIRouter()


@router.get("/listar-usuarios")
def get_list_users():
    """"""
    return [{"usuarios": ""}]


@router.post("/crear-usuarios")
def create_users():
    """"""
    return [{"usuarios": ""}]


@router.put("/modificar-usuarios")
def edit_users():
    """"""
    return [{"usuarios": ""}]
