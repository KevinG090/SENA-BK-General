error_msg_templates = {
    # Errores de cadena de texto
    'value_error.any_str.max_length': 'max_length:{limit_value}',
    'value_error.any_str.min_length': 'min_length:{limit_value}',
    'value_error.any_str.empty': 'El campo no puede estar vacío',
    'value_error.any_str.strip': 'strip:{original_value} (valor original)',  # Personalizar si se desea
    'value_error.regex': 'El valor no coincide con el formato esperado',
    'value_error.email': 'El correo electrónico no tiene un formato válido',
    'value_error.url': 'La URL no tiene un formato válido',

    # Errores de números
    'value_error.number.not_gt': 'not_greater_than:{limit_value}',
    'value_error.number.not_ge': 'not_greater_than_or_equal:{limit_value}',
    'value_error.number.not_lt': 'not_less_than:{limit_value}',
    'value_error.number.not_le': 'not_less_than_or_equal:{limit_value}',
    'value_error.number.not_int': 'El valor no es un número entero',
    'value_error.number.not_float': 'El valor no es un número decimal',

    # Errores de tipo
    'value_error.dict': 'El valor no es un diccionario',
    'value_error.list': 'El valor no es una lista',
    'value_error.none.not_allowed': 'El valor None no está permitido',
    'value_error.str': 'El valor no es una cadena de texto',

    # Errores de valores específicos
    'value_error.json': 'El valor no es un JSON válido',
    'value_error.enum': 'El valor no es una opción válida del enumerado',
    'value_error.datetime': 'El valor no tiene un formato de fecha y hora válido',
    'value_error.date': 'El valor no tiene un formato de fecha válido',
    'value_error.time': 'El valor no tiene un formato de hora válido',
    'value_error.timedelta': 'El valor no tiene un formato de intervalo de tiempo válido',
    'value_error.bytes': 'El valor no es una secuencia de bytes válida',
    'value_error.decimal': 'El valor no es un decimal válido',
    'value_error.uuid': 'El valor no es un UUID válido',
    'value_error.ipv4': 'El valor no es una dirección IPv4 válida',
    'value_error.ipv6': 'El valor no es una dirección IPv6 válida',
    'value_error.ip_address': 'El valor no es una dirección IP válida',
    'value_error.color': 'El valor no tiene un formato de color válido',


    'value_error.missing': 'El campo es requerido',
    'value_error.unexpected': 'Error inesperado',
    'value_error.foreign_key': 'Valor no válido para la clave foránea',
    'value_error.unique': 'El valor ya existe',

    'type_error.str': 'se_esperaba_una_cadena',
    'type_error.int': 'se_esperaba_un_entero',
    'type_error.float': 'se_esperaba_un_flotante',
    'type_error.bool': 'se_esperaba_un_booleano',
    'type_error.list': 'se_esperaba_una_lista',
    'type_error.dict': 'se_esperaba_un_diccionario',
    'type_error.datetime': 'se_esperaba_una_fecha_hora',
    'type_error.date': 'se_esperaba_una_fecha',
    'type_error.time': 'se_esperaba_una_hora',
    'type_error.decimal': 'se_esperaba_un_decimal',
    'type_error.json': 'se_esperaba_un_json',
    'type_error.url': 'se_esperaba_una_url',
    'type_error.uuid': 'se_esperaba_un_uuid',
    'type_error.path': 'se_esperaba_una_ruta_de_archivo',
    'type_error.email': 'se_esperaba_un_correo_electronico',
    'type_error.ipv4': 'se_esperaba_una_direccion_ipv4',
    'type_error.ipv6': 'se_esperaba_una_direccion_ipv6'
}