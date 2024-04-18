import math
from typing import Any, Dict, List, Optional

from psycopg.rows import dict_row

from db.connection import pool_dispatcher


class CursosQueries:
    """Clase para queries de los cursos"""

    @staticmethod
    async def lista_paginada_cursos(
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
        query_pag = f"""
            SELECT COUNT(*)
            FROM ({query}) AS subconsulta;
        """

        async with pool_dispatcher.async_pool.read.connection() as conn:
            async with conn.cursor(
                name="search_cursos_paginados", scrollable=True
            ) as cursor:
                cursor.row_factory = dict_row
                await cursor.execute(query, data)
                await cursor.scroll(offset)

                res: List[Dict[str, Any]] = await cursor.fetchmany(limit)

                results = {"next_exist": bool(await cursor.fetchone()), "results": res}

                await cursor.execute(query_pag, data)

                res_count: Any | dict[str, Any] = await cursor.fetchone()
                max_elems = res_count.get("count", len(res))
                max_pages = math.ceil(max_elems / limit)

                results.update(
                    {
                        "max_elems": max_elems,
                        "max_pages": max_pages,
                    }
                )

                return results
