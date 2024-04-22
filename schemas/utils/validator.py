
def validate_type_number(value:str):
    try:
        return int(str(value))
    except ValueError as exc:
        raise ValueError("campo debe ser numerico") from exc