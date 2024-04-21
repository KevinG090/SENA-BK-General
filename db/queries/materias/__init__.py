import math
import json
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Dict, Any, Generator, Optional, List, Literal, Union

from psycopg2 import sql, extras
from psycopg2.extensions import register_adapter
from psycopg.rows import dict_row
from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from db.utils import Json_pyscopg2

class MateriasQueries(Connection):
    """Clase para queries de los materias"""
    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)

    # @staticmethod
    async def lista_paginada_materias(
        self,
        limit: int = 10,
        offset: int = 0,
        pk_id_materia: Optional[str] = None,
        nombre_materia: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "pk_id_materia": pk_id_materia,
            "nombre_materia": (
                nombre_materia.upper() if not nombre_materia is None else None
            ),
        }

        query = """
            SELECT
                pk_id_materia,
                nombre_materia
            FROM public.tbl_materias
            WHERE
                pk_id_materia::TEXT LIKE COALESCE(
                    '%%'||%(pk_id_materia)s||'%%',
                    pk_id_materia::TEXT
                )
                AND UPPER(nombre_materia) LIKE COALESCE(
                    '%%'||%(nombre_materia)s||'%%',
                    UPPER(nombre_materia)
                )
            ORDER BY pk_id_materia DESC
        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(
                cursor_factory=RealDictCursor,
                name="consulta_paginada_materias",
                scrollable=True,
            ) as cursor:
                cursor.execute(query, data)
                cursor.scroll(offset)

                res: List[RealDictRow] = cursor.fetchmany(limit)

                results = {"next_exist": bool(cursor.fetchone()), "results": res}

                return results
