import json

from datetime import datetime
from decimal import Decimal
from typing import Any, List

from psycopg2 import extras


class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class Json_pyscopg2(extras.Json):
    def dumps(self, obj: Any):
        return json.dumps(obj, cls=JSONEncoder)


def list_to_json(lista: List[Any], seqToReplace: str = ""):
    arr: List[Any] = []
    for val in lista:
        arr.append(f"{adaptType(val, seqToReplace)}")

    arr_text = f'json_build_array({",".join(arr)})'
    return arr_text


def dict_to_sqljson(obj: dict[Any, Any], seqToReplace: str = ""):
    arr: List[Any] = []
    for key in obj:
        arr.append(f"'{key}',{adaptType(obj[key], seqToReplace)}")

    obj_text = f'json_build_object({",".join(arr)})'
    return obj_text


def adaptType(val: Any, seqToReplace: str = ""):
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


def adaptTypes(values: Any, seqToReplace: str = ""):
    arr: List[Any] = []
    for val in values:
        arr.append(adaptType(val, seqToReplace))

    arr_text = f"{','.join(arr)}"
    return arr_text
