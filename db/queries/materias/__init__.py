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


class MateriasQueries(Connection):
    """Clase para queries de los materias"""

    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)

    # @staticmethod
    async def lista_paginada_materias_cursos(
        self,
        limit: int = 10,
        offset: int = 0,
        pk_id_materia: Optional[str] = None,
        nombre_materia: Optional[str] = None,
        pk_id_curso: Optional[str] = None,
        nombre_curso: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {
            "pk_id_materia": pk_id_materia,
            "nombre_materia": (
                nombre_materia.upper() if not nombre_materia is None else None
            ),
            "pk_id_curso": pk_id_curso,
            "nombre_curso": nombre_curso.upper() if not nombre_curso is None else None,
        }

        query = """
            SELECT
                tbl_materias.*,
				tbl_cursos.pk_id_curso,
				tbl_cursos.nombre_curso,
                u_tbl_cursos_materias.pk_relacion_curso_materia
            FROM public.tbl_materias
            INNER JOIN u_tbl_cursos_materias ON (
                tbl_materias.pk_id_materia = u_tbl_cursos_materias.fk_id_materia
            )
            INNER JOIN tbl_cursos ON (
                u_tbl_cursos_materias.fk_id_curso = tbl_cursos.pk_id_curso
            )
            WHERE
                pk_id_materia::TEXT LIKE COALESCE(
                    '%%'||%(pk_id_materia)s||'%%',
                    pk_id_materia::TEXT
                )
                AND UPPER(nombre_materia) LIKE COALESCE(
                    '%%'||%(nombre_materia)s||'%%',
                    UPPER(nombre_materia)
                )
                AND pk_id_curso::TEXT LIKE COALESCE(
                    '%%'||%(pk_id_curso)s||'%%',
                    pk_id_curso::TEXT
                )
                AND UPPER(nombre_curso) LIKE COALESCE(
                    '%%'||%(nombre_curso)s||'%%',
                    UPPER(nombre_curso)
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
                *
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
        with self._open_connection() as conexion:
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

    async def asignar_curso_materias(
        self, pk_id_materia: int, pk_id_curso: int
    ) -> Dict[str, Any]:
        """Metodo para asignarle un curso a la materia o a la inversa"""

        query = """
            INSERT INTO public.u_tbl_cursos_materias(
                fk_id_materia,
                fk_id_curso
            )
            VALUES (
                %(fk_id_materia)s,
                %(fk_id_curso)s
            )
            RETURNING pk_relacion_curso_materia;
        """
        with self._open_connection() as conexion:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    query, {"fk_id_materia": pk_id_materia, "fk_id_curso": pk_id_curso}
                )

                res: Union[RealDictRow, None] = cursor.fetchone()

                results = {"results": res}

                return results

    async def eliminar_relacion_curso_materias(
        self, fk_id_materia: int, fk_id_curso: int
    ) -> Dict[str, Any]:
        """Metodo para asignarle un curso a la materia o a la inversa"""

        query = """
            DELETE FROM public.u_tbl_cursos_materias
            WHERE fk_id_materia = %(fk_id_materia)s AND fk_id_curso = %(fk_id_curso)s;
        """
        with self._open_connection() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    query, {"fk_id_materia": fk_id_materia, "fk_id_curso": fk_id_curso}
                )

                return {"delete_item": True}
