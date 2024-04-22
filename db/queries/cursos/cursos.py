from typing import Any, Dict, List, Optional, Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from db.utils import Json_pyscopg2

from schemas.responses_model.cursos import (
    InputCreacionCurso,
)


class CursosQueries(Connection):
    """Clase para queries de los cursos"""

    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)

    # @staticmethod
    async def lista_paginada_cursos(
        self,
        limit: int = 10,
        offset: int = 0,
        pk_id_curso: Optional[str] = None,
        nombre_curso: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "pk_id_curso": pk_id_curso,
            "nombre_curso": nombre_curso.upper() if not nombre_curso is None else None,
        }

        query = """
            SELECT
                pk_id_curso,
                nombre_curso
            FROM public.tbl_cursos
            WHERE
                pk_id_curso::TEXT LIKE COALESCE(
                    '%%'||%(pk_id_curso)s||'%%',
                    pk_id_curso::TEXT
                )
                AND UPPER(nombre_curso) LIKE COALESCE(
                    '%%'||%(nombre_curso)s||'%%',
                    UPPER(nombre_curso)
                )
            ORDER BY pk_id_curso DESC
        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(
                cursor_factory=RealDictCursor,
                name="consulta_paginada_cursos",
                scrollable=True,
            ) as cursor:
                cursor.execute(query, data)
                cursor.scroll(offset)

                res: List[RealDictRow] = cursor.fetchmany(limit)

                results = {"next_exist": bool(cursor.fetchone()), "results": res}

                return results
            
    async def crear_cursos(self, data: InputCreacionCurso) -> Dict[str, Any]:

        query = """INSERT INTO public.tbl_cursos(
                nombre_curso,
            )
            VALUES (
                %(nombre_curso)s,
            )
            RETURNING pk_id_curso;
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute(query, data.dict())

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results