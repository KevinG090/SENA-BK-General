""""""

from typing import Any, Dict, List, Optional

from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection


class EventosQueries(Connection):
    """"""

    async def lista_paginada_eventos(
        self,
        limit: int = 10,
        offset: int = 0,
        fk_id_curso: Optional[str] = None,
        nombre_evento: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "fk_id_curso": fk_id_curso,
            "nombre_evento": (
                nombre_evento.upper() if not nombre_evento is None else None
            ),
        }

        query = """
            SELECT
                *
            FROM public.tbl_eventos
            WHERE
                fk_id_curso::TEXT LIKE COALESCE(
                    '%%'||%(fk_id_curso)s||'%%',
                    fk_id_curso::TEXT
                )
                AND UPPER(nombre_evento) LIKE COALESCE(
                    '%%'||%(nombre_evento)s||'%%',
                    UPPER(nombre_evento)
                )
            ORDER BY pk_id_evento DESC
        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(
                cursor_factory=RealDictCursor,
                name="consulta_paginada_evento",
                scrollable=True,
            ) as cursor:
                cursor.execute(query, data)
                cursor.scroll(offset)

                res: List[RealDictRow] = cursor.fetchmany(limit)

                results = {"next_exist": bool(cursor.fetchone()), "results": res}

                return results
