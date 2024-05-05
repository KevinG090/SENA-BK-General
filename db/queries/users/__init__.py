""""""

from typing import Any, Dict, List, Optional, Union

from psycopg2.extensions import register_adapter
from psycopg2.extras import RealDictCursor, RealDictRow

# from db.connection_optional import Connection
from db.connection_schema import Connection
from db.utils import Json_pyscopg2
from schemas.responses_model.users import InputCreacionUsers

from models import Usuario, UtilsModel


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

        with self._open_connection(1) as conexion:
            query = conexion.query(Usuario)

            if pk_id_usuario is not None:
                query = query.filter(Usuario.pk_id_usuario.like(f"%{pk_id_usuario}%"))
            if nombre_usuario is not None:
                query = query.filter(
                    Usuario.nombre_usuario.ilike(f"%{nombre_usuario.upper()}%")
                )

            # Ordenar los resultados
            query = query.order_by(Usuario.pk_id_usuario.desc())
            # Contar los resultados sin limites
            total = query.count()

            query = query.offset(offset).limit(limit)

            # Obtener los resultados
            res = query.all()
            next_exist = UtilsModel().next_page_exist(total, limit, offset)
            res_dict = [usuario.to_dict(["contraseña"]) for usuario in res]

            results = {"next_exist": next_exist, "results": res_dict}

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
