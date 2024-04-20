""""""

from fastapi import APIRouter
from db.queries.users import Query 

router = APIRouter()


@router.get("/listar-usuarios")
def get_list_users():
    """"""
    query_helper = Query()

    return query_helper.consultar_cursos()


@router.post("/crear-usuarios")
def create_users():
    """"""
    return [{"usuarios": ""}]


@router.put("/modificar-usuarios")
def edit_users():
    """"""
    return [{"usuarios": ""}]
