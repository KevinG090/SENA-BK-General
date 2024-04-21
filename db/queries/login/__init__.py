import math
from typing import Any, Dict, List, Optional, Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg.rows import dict_row

from db.connection_optional import Connection
from db.utils import Json_pyscopg2


class LoginQueries(Connection):
    """Clase para queries de los cursos"""

    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)

    # @staticmethod
    async def buscar_usuario(
        self,
        email: str,
        passworld: str,
    ) -> Union[RealDictRow, None]:
        data = {
            "correo": email,
            "passworld": passworld,
        }

        query = """
            SELECT *
            FROM public.tbl_usuarios AS users
            WHERE
                UPPER(users.correo) LIKE UPPER('%%'||%(correo)s||'%%')
                AND UPPER(users.contraseña) LIKE UPPER('%%'||%(passworld)s||'%%')

        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor, name="login") as cursor:
                cursor.execute(query, data)

                res: Union[RealDictRow, None] = cursor.fetchone()

                return res
