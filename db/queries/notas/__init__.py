""""""

from typing import Any, Dict, List, Optional, Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from db.utils import Json_pyscopg2
from schemas.responses_model.materias import (
    InputCreacionMaterias,
    InputModificacionMateria,
)


class NotasQueries(Connection):
    """Clase para queries de los materias"""

    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)

    # @staticmethod
    async def lista_paginada_notas(
        self,
        limit: int = 10,
        offset: int = 0,
        pk_id_materia: Optional[str] = None,
        nombre_materia: Optional[str] = None,
        pk_id_curso: Optional[str] = None,
        nombre_curso: Optional[str] = None,
        pk_id_usuario: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "pk_id_materia": pk_id_materia,
            "nombre_materia": (
                nombre_materia.upper() if not nombre_materia is None else None
            ),
            "pk_id_curso": pk_id_curso,
            "nombre_curso": (
                nombre_curso.upper() if not nombre_curso is None else None
            ),
            "pk_id_usuario": pk_id_usuario,
        }

        query = """
            SELECT
                tbl_notas.*,
                tbl_usuarios.nombre_usuario,
                tbl_cursos.nombre_curso,
                tbl_materias.nombre_materia
            FROM public.tbl_notas
            INNER JOIN u_tbl_usuarios_cursos ON (
                tbl_notas.fk_relacion_usuario_curso = u_tbl_usuarios_cursos.pk_relacion_usuario_curso
            )
            INNER JOIN tbl_cursos ON (
                tbl_cursos.pk_id_curso = u_tbl_usuarios_cursos.fk_id_curso
            )
            INNER JOIN tbl_usuarios ON (
                u_tbl_usuarios_cursos.fk_id_usuario = tbl_usuarios.pk_id_usuario
            )
            INNER JOIN u_tbl_cursos_materias ON (
                tbl_notas.fk_relacion_curso_materia = u_tbl_cursos_materias.pk_relacion_curso_materia
                AND tbl_cursos.pk_id_curso = u_tbl_cursos_materias.fk_id_curso
                AND u_tbl_usuarios_cursos.fk_id_curso = u_tbl_cursos_materias.fk_id_curso
            )
            INNER JOIN tbl_materias ON (
                u_tbl_cursos_materias.fk_id_materia = tbl_materias.pk_id_materia
            )
            WHERE
                UPPER(nombre_materia) LIKE COALESCE(
                    '%%'||%(nombre_materia)s||'%%',
                    UPPER(nombre_materia)
                )
                AND UPPER(nombre_curso) LIKE COALESCE(
                    '%%'||%(nombre_curso)s||'%%',
                    UPPER(nombre_curso)
                )
                AND pk_id_materia = COALESCE(
                    %(pk_id_materia)s,
                    pk_id_materia
                )
                AND pk_id_curso = COALESCE(
                    %(pk_id_curso)s,
                    pk_id_curso
                )
                AND pk_id_usuario = COALESCE(
                    %(pk_id_usuario)s,
                    pk_id_usuario
                )
            ORDER BY pk_id_nota DESC
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

    async def crear_materias(self, data: InputCreacionMaterias) -> Dict[str, Any]:
        query = """
            INSERT INTO public.tbl_materias(
                nombre_materia,
                descripcion
            )
            VALUES (
                %(nombre_materia)s,
                %(descripcion)s
            )
            RETURNING pk_id_materia;
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, data.dict())

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def verificar_materias(self, pk_id_materia: str) -> Dict[str, Any]:
        query = """
            SELECT *
            FROM public.tbl_materias
            WHERE
                pk_id_materia = %(pk_id_materia)s
            ORDER BY pk_id_materia DESC
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query,
                    {
                        "pk_id_materia": pk_id_materia,
                    },
                )

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def modificar_materias(
        self, pk_id_materia: str, data: InputModificacionMateria
    ) -> Dict[str, Any]:
        query = """
            UPDATE public.tbl_materias
            SET
                nombre_materia = %(nombre_materia)s,
                descripcion = %(descripcion)s
            WHERE
                pk_id_materia = %(pk_id_materia)s
            RETURNING pk_id_materia;
        """
        with self._open_connection() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query,
                    {
                        "pk_id_materia": pk_id_materia,
                        "nombre_materia": data.nombre_materia,
                        "descripcion": data.descripcion,
                    },
                )

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results
