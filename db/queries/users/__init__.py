import math
import json
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Dict, Any, Generator, Optional, List, Literal, Union


from decimal import Decimal


from psycopg2 import sql, extras
from psycopg2.extensions import register_adapter

from db.connection_optional import Connection

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class Json_pyscopg2(extras.Json):
    def dumps(self, obj):
        return json.dumps(obj, cls=JSONEncoder)


def list_to_json(lista, seqToReplace=""):
    arr = []
    for val in lista:
        arr.append(f"{adaptType(val, seqToReplace)}")

    arr_text = f'json_build_array({",".join(arr)})'
    return arr_text


def dict_to_sqljson(obj, seqToReplace=""):
    arr = []
    for key in obj:
        arr.append(f"'{key}',{adaptType(obj[key], seqToReplace)}")

    obj_text = f'json_build_object({",".join(arr)})'
    return obj_text


def adaptType(val, seqToReplace=""):
    if isinstance(val, (bool)):
        arr = f"{'true' if val else 'false'}"
    elif val == "next_id_trx":
        arr = f"NEXTVAL('{seqToReplace}')"
    elif isinstance(val, (int, float)) or val == "new_id_trx":
        arr = f"{val}"
    elif isinstance(val, (dict)):
        arr = f"{dict_to_sqljson(val, seqToReplace)}"
    elif isinstance(val, (list)):
        arr = f"{list_to_json(val, seqToReplace)}"
    elif isinstance(val, (str)) and val.find("new_id_trx") != -1:
        arrOcc = val.replace("'", '"').replace("new_id_trx", "|new_id_trx|").split("|")
        for it in range(len(arrOcc)):
            if arrOcc[it] != "new_id_trx":
                arrOcc[it] = f"'{arrOcc[it]}'"
        strOcc = ",".join(arrOcc)
        arr = f"CONCAT({strOcc})"
    else:
        newval = str(val).replace("'", '"')
        arr = f"'{newval}'"

    return arr


def adaptTypes(values, seqToReplace=""):
    arr = []
    for val in values:
        arr.append(adaptType(val, seqToReplace))

    arr_text = f"{','.join(arr)}"
    return arr_text


class Query(Connection):
    def __init__(self) -> None:
        super().__init__()
        register_adapter(dict, Json_pyscopg2)
   
    def consultar_cursos(self):

        query = f"""
            SELECT
                pk_id_curso,
                nombre_curso
            FROM public.tbl_cursos
        """

        conexion = self.connect()
        try:
            cursor = conexion.cursor()

            cursor.execute(query)
            conexion.commit()

            cols = [obj[0] for obj in cursor.description]
            Lista = [
                {cols[index]: val for index, val in enumerate(obj)}
                for obj in cursor.fetchall()
            ]


            # self.closeConnection(conexion)
            return Lista
        except Exception as e:
            self.closeConnection(conexion)
            raise e