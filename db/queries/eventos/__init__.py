""""""

from typing import Any, Dict, List, Optional, Union

from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from schemas.responses_model.eventos import InputCreacionEvento, InputModificacionEventos


class EventosQueries(Connection):
    """"""

    async def lista_paginada_eventos(
        self,
        limit: int = 10,
        offset: int = 0,
        fk_id_curso: Optional[str] = None,
        nombre_evento: Optional[str] = None,
        pk_id_evento: Optional[str] = None,
    ) -> Dict[str, Any]:
        condition = [
            "pk_id_evento::TEXT LIKE"
            " COALESCE('%%'||%(pk_id_evento)s||'%%',pk_id_evento::TEXT)"
        ]
        data = {"pk_id_evento": pk_id_evento}

        if not fk_id_curso is None:
            data.update({"fk_id_curso": fk_id_curso})
            condition.append(
                "fk_id_curso::TEXT LIKE"
                " COALESCE('%%'||%(fk_id_curso)s||'%%',fk_id_curso::TEXT)"
            )
        if not nombre_evento is None:
            data.update({"nombre_evento": nombre_evento.upper()})
            condition.append(
                "nombre_evento::TEXT LIKE"
                " COALESCE('%%'||%(nombre_evento)s||'%%',nombre_evento::TEXT)"
            )

        query = f"""
            SELECT
                *
            FROM public.tbl_eventos
            WHERE {' AND '.join(condition)}
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

    async def crear_eventos(self, data: InputCreacionEvento) -> Dict[str, Any]:
        query = """
            INSERT INTO public.tbl_eventos(
                fk_id_curso,
                nombre_evento,
                contenido
            )
            VALUES (
                %(fk_id_curso)s,
                %(nombre_evento)s,
                %(contenido)s
            )
            RETURNING pk_id_evento;
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, data.dict())

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results
            
    async def verificar_eventos(self, pk_id_evento: str) -> Dict[str, Any]:
        query = """
            SELECT *
            FROM public.tbl_eventos
            WHERE
                pk_id_evento = %(pk_id_evento)s
            ORDER BY pk_id_evento DESC
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, {
                    "pk_id_evento":pk_id_evento,
                })

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def modificar_eventos(self, pk_id_evento: str,data: InputModificacionEventos) -> Dict[str, Any]:
        query = """
            UPDATE public.tbl_eventos
            SET 
                fk_id_curso = %(fk_id_curso)s,
                nombre_evento = %(nombre_evento)s,
                contenido = %(contenido)s
            WHERE
                pk_id_evento = %(pk_id_evento)s
            RETURNING pk_id_evento;
        """
        with self._open_connection() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, {
                    "pk_id_evento":pk_id_evento,
                    "fk_id_curso":data.fk_id_curso,
                    "nombre_evento":data.nombre_evento,
                    "contenido":data.contenido
                })

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results