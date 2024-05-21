""""""

from typing import Any, Dict, List, Optional, Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow

from db.connection_optional import Connection
from db.utils import Json_pyscopg2
from schemas.responses_model.notas import (
    InputCreacionNota,
    InputModificacionNota,
)


class NotasQueries(Connection):
    """Clase para queries de los notas"""

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
                ARRAY_AGG(tbl_notas.nota) AS notas,
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
            GROUP BY
				tbl_usuarios.nombre_usuario,
				tbl_usuarios.pk_id_usuario,
				tbl_cursos.nombre_curso,
				tbl_materias.nombre_materia,
				tbl_materias.pk_id_materia
            ORDER BY notas DESC
        """

        with self._open_connection(1) as conexion:
            with conexion.cursor(
                cursor_factory=RealDictCursor,
                name="consulta_paginada_notas",
                scrollable=True,
            ) as cursor:
                cursor.execute(query, data)
                cursor.scroll(offset)

                res: List[RealDictRow] = cursor.fetchmany(limit)

                results = {"next_exist": bool(cursor.fetchone()), "results": res}

                return results

    async def verificar_config_estudiante(
        self, pk_relacion_usuario_curso: int, pk_relacion_curso_materia: int
    ) -> Dict[str, Any]:
        query = """
            SELECT 
                tbl_usuarios.pk_id_usuario,
                tbl_usuarios.nombre_usuario,
                tbl_materias.nombre_materia,
                tbl_cursos.nombre_curso
            FROM public.tbl_usuarios
            INNER JOIN u_tbl_usuarios_cursos ON (
                tbl_usuarios.pk_id_usuario = u_tbl_usuarios_cursos.fk_id_usuario
            )
            INNER JOIN u_tbl_cursos_materias ON (
                u_tbl_usuarios_cursos.fk_id_curso = u_tbl_cursos_materias.fk_id_curso
            )
            INNER JOIN tbl_cursos ON (
                u_tbl_usuarios_cursos.fk_id_curso = tbl_cursos.pk_id_curso
                AND u_tbl_usuarios_cursos.fk_id_curso = tbl_cursos.pk_id_curso
            )
            INNER JOIN tbl_materias ON (
                u_tbl_cursos_materias.fk_id_materia = tbl_materias.pk_id_materia
            )
            WHERE
                pk_relacion_usuario_curso = %(pk_relacion_usuario_curso)s
                AND pk_relacion_curso_materia = %(pk_relacion_curso_materia)s
            ORDER BY pk_id_usuario DESC
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query,
                    {
                        "pk_relacion_usuario_curso": pk_relacion_usuario_curso,
                        "pk_relacion_curso_materia": pk_relacion_curso_materia,
                    },
                )

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def crear_notas(self, data: InputCreacionNota) -> Dict[str, Any]:
        query = """
            INSERT INTO public.tbl_notas(
                nota,
                observaciones,
                fk_relacion_usuario_curso,
                fk_relacion_curso_materia
            )
            VALUES (
                %(nota)s,
                %(observaciones)s,
                %(fk_relacion_usuario_curso)s,
                %(fk_relacion_curso_materia)s
            )
            RETURNING pk_id_nota;
        """
        with self._open_connection(1) as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, data.dict())

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def modificar_notas(
        self, pk_id_nota: str, data: InputModificacionNota
    ) -> Dict[str, Any]:
        query = """
            UPDATE public.tbl_notas
            SET
                nota = %(nota)s
            WHERE
                pk_id_nota = %(pk_id_nota)s
            RETURNING pk_id_nota;
        """
        with self._open_connection() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query,
                    {"pk_id_nota": pk_id_nota, "nota": data.nota},
                )

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results
