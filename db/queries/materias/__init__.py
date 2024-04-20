import math
from typing import Any, Dict, List, Optional

from psycopg.rows import dict_row

from db.connection import pool_dispatcher


class MateriasQueries:
    """Clase para queries de los materias"""

    @staticmethod
    async def lista_paginada_materias(
        limit: int = 10,
        offset: int = 0,
        pk_id_materias: Optional[str] = None,
        nombre_materias: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "pk_id_materias": pk_id_materias,
            "nombre_materias": (
                nombre_materias.upper() if not nombre_materias is None else None
            ),
        }

        query = """
            SELECT
                pk_id_materias,
                nombre_materias
            FROM public.tbl_cursos
            WHERE
                pk_id_materias::TEXT LIKE COALESCE(
                    '%%'||%(pk_id_materias)s||'%%',
                    pk_id_materias::TEXT
                )
                AND UPPER(nombre_materias) LIKE COALESCE(
                    '%%'||%(nombre_materias)s||'%%',
                    UPPER(nombre_materias)
                )
            ORDER BY pk_id_materias DESC
        """
        query_pag = f"""
            SELECT COUNT(*)
            FROM ({query}) AS subconsulta;
        """

        async with pool_dispatcher.async_pool.read.connection() as conn:
            async with conn.cursor(
                name="search_materias_paginados", scrollable=True
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
