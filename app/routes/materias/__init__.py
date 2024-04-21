""""""

from fastapi import APIRouter
from psycopg.errors import Error as PGError

from db.queries.materias import MateriasQueries
from schemas.responses_model.common import EnumErrors, EnumMsg, ResponseBase

router = APIRouter()


@router.get("/listar-materias")
async def get_list_topics():
    """"""
    try:
        results = await MateriasQueries().lista_paginada_materias()
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


@router.post("/crear-materias")
async def create_topics():
    """"""
    return [{"materias": ""}]


@router.put("/modificar-materias")
async def edit_topics():
    """"""
    return [{"materias": ""}]
