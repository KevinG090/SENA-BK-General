""""""

from typing import Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from db.utils import Json_pyscopg2


class LoginQueries(Connection):
    """Clase para queries de los cursos"""

    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)

    # @staticmethod
    async def login_usuario(
        self,
        email: str,
        password: str,
    ) -> Union[RealDictRow, None]:
        data = {
            "correo": email,
            "password": password,
        }

        query = """
            SELECT
                tbl_tipo_usuarios.*,
                users.pk_id_usuario,
                users.celular,
                users.identificacion,
                users.pk_id_usuario,
                users.observaciones,
                users.nombre_usuario,
                COALESCE(tbl_cursos.nombre_curso,null) AS nombre_curso,
				COALESCE(tbl_cursos.pk_id_curso,null) AS pk_id_curso,
                users.correo
            FROM public.tbl_usuarios AS users
            INNER JOIN public.tbl_tipo_usuarios
                ON (users.fk_id_tipo_usuario =  tbl_tipo_usuarios.pk_id_tipo_usuario)
            LEFT JOIN u_tbl_usuarios_cursos ON (
				users.pk_id_usuario = u_tbl_usuarios_cursos.fk_id_usuario
			)
			LEFT JOIN tbl_cursos ON (
				u_tbl_usuarios_cursos.fk_id_curso = tbl_cursos.pk_id_curso
			)
            WHERE
                UPPER(users.correo) LIKE UPPER(%(correo)s)
                AND users.contraseña = %(password)s

        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor, name="login") as cursor:
                cursor.execute(query, data)

                res: Union[RealDictRow, None] = cursor.fetchone()

                return res

    async def buscar_usuario(
        self,
        pk_id_usuario: int,
    ) -> Union[RealDictRow, None]:
        data = {
            "pk_id_usuario": pk_id_usuario,
        }

        query = """
            SELECT
                tbl_tipo_usuarios.*,
                users.pk_id_usuario,
                users.celular,
                users.identificacion,
                users.pk_id_usuario,
                users.observaciones,
                users.nombre_usuario,
                COALESCE(tbl_cursos.nombre_curso,null) AS nombre_curso,
				COALESCE(tbl_cursos.pk_id_curso,null) AS pk_id_curso,
                users.correo
            FROM public.tbl_usuarios AS users
            INNER JOIN public.tbl_tipo_usuarios
                ON (users.fk_id_tipo_usuario =  tbl_tipo_usuarios.pk_id_tipo_usuario)
			LEFT JOIN u_tbl_usuarios_cursos ON (
				users.pk_id_usuario = u_tbl_usuarios_cursos.fk_id_usuario
			)
			LEFT JOIN tbl_cursos ON (
				u_tbl_usuarios_cursos.fk_id_curso = tbl_cursos.pk_id_curso
			)
            WHERE
                users.pk_id_usuario = %(pk_id_usuario)s
        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(
                cursor_factory=RealDictCursor, name="search_user"
            ) as cursor:
                cursor.execute(query, data)

                res: Union[RealDictRow, None] = cursor.fetchone()

                return res
