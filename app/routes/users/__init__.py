""""""

from fastapi import APIRouter
from db.queries.users import UsersQueries
from psycopg.errors import Error as PGError

from schemas.responses_model.common import EnumErrors, ResponseBase, EnumMsg

router = APIRouter()


@router.get("/listar-usuarios")
async def get_list_users():
    """"""
    try:
        results = await UsersQueries().consultar_paginada_usuarios()
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


@router.post("/crear-usuarios")
async def create_users():
    """"""
    return [{"usuarios": ""}]


@router.put("/modificar-usuarios")
async def edit_users():
    """"""
    return [{"usuarios": ""}]
