""" Custom error handlers for common errors """

from typing import Dict, Any, Union, Type

from asyncpg.exceptions._base import PostgresError
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg.errors import Error as PGError
from pydantic_core import ValidationError

from schemas.responses_model.common import (
    DetailErrorObj,
    ErrorResponse,
    ResponseBaseError,
    ResponseBase
)


def format_error(exc: RequestValidationError) -> Dict[str, str]:
    """Give format to Validations error for better messages"""

    reformatted_message = {}
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join([str(_loc) for _loc in filtered_loc])
        reformatted_message[field_string] = msg

    return reformatted_message


async def custom_except_handler(_request: Request, exc: ErrorResponse):
    """Function for handle automaticly the custom exceptions 'ErrorResponse'"""
    return JSONResponse(exc.args[0].dict(), exc.args[1])


async def pg_except_handler(request: Request, exc: PGError):
    """Function for handle automaticly psycopg 'Error'"""

    new_exc = ErrorResponse(
        "Peticion fallida",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        DetailErrorObj(
            complete_info=str(exc),
            user_msg="Error en la ejecucion de la query (sync)",
        ),
    )
    return await custom_except_handler(request, new_exc)


async def db_except_handler(request: Request, exc: PostgresError):
    """Function for handle automaticly the base 'PostgresError'"""
    # print(exc.__class__.__bases__, end="\n\n\n")
    new_exc = ErrorResponse(
        "Peticion fallida",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        DetailErrorObj(
            complete_info=f"{exc}",
            user_msg="Error durante la ejecucion de la query (async)",
        ),
    )
    return await custom_except_handler(request, new_exc)


async def validation_except_handler(request: Request, exc: ValidationError):
    """Function for handle automaticly pydantic 'ValidationError'"""

    new_exc = ErrorResponse(
        "Peticion fallida",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        DetailErrorObj(
            complete_info=str(exc),
            user_msg="Entrada de datos invalida",
        ),
    )
    return await custom_except_handler(request, new_exc)


async def unhandled_except_handler(request: Request, exc: Exception):
    """Function for handle automaticly the base 'Exception'"""
    new_exc = ErrorResponse(
        "Peticion fallida",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        DetailErrorObj(
            complete_info=str(exc),
            user_msg="Error error sin controlar durante la ejecucion",
        ),
    )
    return await custom_except_handler(request, new_exc)


async def request_validation_except_handler(
    request: Request, exc: RequestValidationError
):
    """Function for handle automaticly fastapi 'RequestValidationError'"""

    new_exc = ErrorResponse(
        "Peticion fallida",
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        DetailErrorObj(
            complete_info=format_error(exc),
            user_msg="Entrada de datos invalida",
        ),
    )
    return await custom_except_handler(request, new_exc)


def init_handlers(application: FastAPI):
    """Exception handlers to fast api app"""

    application.add_exception_handler(PGError, pg_except_handler)
    application.add_exception_handler(PostgresError, db_except_handler)
    application.add_exception_handler(ErrorResponse, custom_except_handler)
    application.add_exception_handler(ValidationError, validation_except_handler)
    application.add_exception_handler(Exception, unhandled_except_handler)
    application.add_exception_handler(
        RequestValidationError, request_validation_except_handler
    )


responses_handlers: Dict[Union[int, str], Dict[str, Type]] = {
    status.HTTP_200_OK: {"model": ResponseBase},
    status.HTTP_400_BAD_REQUEST: {"model": ResponseBaseError},
    # status.HTTP_401_UNAUTHORIZED: {"model": ResponseBaseError},
    # status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ResponseBaseError},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseBaseError},
    # status.HTTP_502_BAD_GATEWAY: {"model": ResponseBaseError},
}
