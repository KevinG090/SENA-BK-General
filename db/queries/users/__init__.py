""""""

from typing import Any, Dict, List, Optional, Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from db.utils import Json_pyscopg2
from schemas.responses_model.users import InputCreacionUsers


class UsersQueries(Connection):
    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)

    async def consultar_paginada_usuarios(
        self,
        limit: int = 10,
        offset: int = 0,
        pk_id_usuario: Optional[str] = None,
        nombre_usuario: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "pk_id_usuario": pk_id_usuario,
            "nombre_usuario": (
                nombre_usuario.upper() if not nombre_usuario is None else None
            ),
        }

        query = """
            SELECT
                pk_id_usuario,
                nombre_usuario
            FROM public.tbl_usuarios
            WHERE
                pk_id_usuario::TEXT LIKE COALESCE(
                    '%%'||%(pk_id_usuario)s||'%%',
                    pk_id_usuario::TEXT
                )
                AND UPPER(nombre_usuario) LIKE COALESCE(
                    '%%'||%(nombre_usuario)s||'%%',
                    UPPER(nombre_usuario)
                )
            ORDER BY pk_id_usuario DESC
        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(
                cursor_factory=RealDictCursor,
                name="consulta_paginada_usuarios",
                scrollable=True,
            ) as cursor:
                cursor.execute(query, data)
                cursor.scroll(offset)

                res: List[RealDictRow] = cursor.fetchmany(limit)

                results = {"next_exist": bool(cursor.fetchone()), "results": res}

                return results

    async def crear_usuarios(self, data: InputCreacionUsers) -> Dict[str, Any]:
        query = """INSERT INTO public.tbl_usuarios(
                nombre_usuario,
                celular,
                correo,
                identificacion,
                contraseña,
                fk_id_tipo_usuario
            )
            VALUES (
                %(nombre_usuario)s,
                %(celular)s,
                %(correo)s,
                %(identificacion)s,
                %(contraseña)s,
                %(fk_id_tipo_usuario)s
            )
            RETURNING pk_id_usuario;
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, data.dict())

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results
