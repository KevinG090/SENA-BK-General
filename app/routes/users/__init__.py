""""""

from fastapi import APIRouter
from psycopg.errors import Error as PGError

from db.queries.users import UsersQueries
from schemas.responses_model.common import EnumErrors, EnumMsg, ResponseBase
from typing import Optional

router = APIRouter()


@router.get("/listar-usuarios")
async def get_list_users(
    limit: int = 10,
    page: int = 1,
    pk_id_usuario: Optional[str] = None,
    nombre_usuario: Optional[str] = None,
):
    """"""
    try:
        offset = (page - 1) * limit
        results = await UsersQueries().consultar_paginada_usuarios(
            limit,
            offset,
            pk_id_usuario,
            nombre_usuario,
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


@router.post("/crear-usuarios")
async def create_users():
    """"""
    return [{"usuarios": ""}]


@router.put("/modificar-usuarios")
async def edit_users():
    """"""
    return [{"usuarios": ""}]
