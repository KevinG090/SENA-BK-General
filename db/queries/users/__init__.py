""""""

from typing import Any, Dict, List, Optional, Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from db.utils import Json_pyscopg2
from schemas.responses_model.users import InputCreacionUsers, InputModificacionUsuario


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
        pk_id_curso: Optional[str] = None,
    ) -> Dict[str, Any]:

        conditions = [
            " pk_id_usuario::TEXT LIKE COALESCE('%%'||%(pk_id_usuario)s||'%%',pk_id_usuario::TEXT)",
            " UPPER(nombre_usuario) LIKE COALESCE('%%'||%(nombre_usuario)s||'%%',UPPER(nombre_usuario))",
        ]
        data = {
            "pk_id_usuario": pk_id_usuario,
            "nombre_usuario": (
                nombre_usuario.upper() if not nombre_usuario is None else None
            ),
        }
        if pk_id_curso:
            data.update({"pk_id_curso": pk_id_curso,})
            conditions.append("pk_id_curso = COALESCE(%(pk_id_curso)s,pk_id_curso)")

        query = f"""
            SELECT
                pk_id_usuario,
                nombre_usuario,
                correo,
                fk_id_tipo_usuario,
                tbl_tipo_usuarios.nombre_tipo_usuario AS tipo_usuario,
                COALESCE(u_tbl_usuarios_cursos.pk_relacion_usuario_curso,null) as pk_relacion_usuario_cursos
            FROM public.tbl_usuarios
            INNER JOIN tbl_tipo_usuarios
                ON (tbl_usuarios.fk_id_tipo_usuario = tbl_tipo_usuarios.pk_id_tipo_usuario)
            LEFT JOIN u_tbl_usuarios_cursos ON (
                tbl_usuarios.pk_id_usuario = u_tbl_usuarios_cursos.fk_id_usuario
            )
            LEFT JOIN tbl_cursos ON (
                u_tbl_usuarios_cursos.fk_id_curso = tbl_cursos.pk_id_curso
            )
            WHERE {"AND ".join(conditions)}
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

    async def verificar_usuarios(self, pk_id_usuario: str) -> Dict[str, Any]:
        query = """
            SELECT
                pk_id_usuario,
                nombre_usuario,
                celular,
                correo,
                identificacion,
                observaciones,
                fk_id_tipo_usuario,
                COALESCE(u_tbl_usuarios_cursos.fk_id_curso,null) AS fk_id_curso 
            FROM public.tbl_usuarios
            LEFT JOIN u_tbl_usuarios_cursos ON (
                tbl_usuarios.pk_id_usuario = u_tbl_usuarios_cursos.fk_id_usuario
            )
            WHERE
                pk_id_usuario = %(pk_id_usuario)s
            ORDER BY pk_id_usuario DESC
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query,
                    {
                        "pk_id_usuario": pk_id_usuario,
                    },
                )

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def modificar_usuarios(
        self, pk_id_usuario: str, data: InputModificacionUsuario
    ) -> Dict[str, Any]:
        query = """
            UPDATE public.tbl_usuarios
            SET
                nombre_usuario = COALESCE(
                    %(nombre_usuario)s,nombre_usuario
                ),
                celular = COALESCE(
                    %(celular)s,celular
                ),
                correo = COALESCE(
                    %(correo)s,correo
                ),
                identificacion = COALESCE(
                    %(identificacion)s,identificacion
                ),
                contraseña = COALESCE(
                    %(contraseña)s,contraseña
                ),
                fk_id_tipo_usuario = COALESCE(
                    %(fk_id_tipo_usuario)s,fk_id_tipo_usuario
                )
            WHERE
                pk_id_usuario = %(pk_id_usuario)s
            RETURNING pk_id_usuario;
        """
        with self._open_connection() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, {"pk_id_usuario": pk_id_usuario, **data.dict()})

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def asignar_curso_usuario(
        self, pk_id_usuario: int, pk_id_curso: int
    ) -> Dict[str, Any]:
        """Metodo para asignarle un curso al usuario"""

        query = """
            INSERT INTO public.u_tbl_usuarios_cursos(
                fk_id_usuario,
                fk_id_curso
            )
            VALUES (
                %(fk_id_usuario)s,
                %(fk_id_curso)s
            )
            RETURNING pk_relacion_usuario_curso;
        """
        with self._open_connection() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query, {"fk_id_usuario": pk_id_usuario, "fk_id_curso": pk_id_curso}
                )

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def eliminar_relacion_curso_usuario(
        self, fk_id_usuario: int, fk_id_curso: int
    ) -> Dict[str, Any]:
        """Metodo para asignarle un curso al usuario"""

        query = """
            DELETE FROM public.u_tbl_usuarios_cursos
            WHERE fk_id_usuario = %(fk_id_usuario)s AND fk_id_curso = %(fk_id_curso)s;
        """
        with self._open_connection() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    query, {"fk_id_usuario": fk_id_usuario, "fk_id_curso": fk_id_curso}
                )
                
                return {"delete_item":True}
