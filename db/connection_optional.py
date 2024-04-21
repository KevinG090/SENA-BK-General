import logging
from contextlib import contextmanager
from typing import Generator, List, Optional, TypedDict, Union

import psycopg2
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import LoggingConnection, RealDictConnection

from core.config import get_settings


class LoggingRealDictConnection(RealDictConnection, LoggingConnection):
    """Get a logged connection and a dict response"""


class DBInitData(TypedDict):
    user: str
    password: str
    host: str
    port: Union[str, int]
    database: str


def getDBInfo():
    users = [get_settings().POSTGRES_WRITE_USER, get_settings().POSTGRES_READ_USER]
    passwords = [
        get_settings().POSTGRES_WRITE_PASSWORD,
        get_settings().POSTGRES_READ_PASSWORD,
    ]
    hosts = [get_settings().POSTGRES_WRITE_SERVER, get_settings().POSTGRES_READ_SERVER]
    ports = [get_settings().POSTGRES_WRITE_PORT, get_settings().POSTGRES_READ_PORT]
    databases = [get_settings().POSTGRES_WRITE_DB, get_settings().POSTGRES_READ_DB]

    lenadbs = max(len(users), len(passwords), len(hosts), len(ports), len(databases))

    def safe_list_get(lst, idx, default=None):
        try:
            return lst[idx]
        except IndexError:
            return default

    available_dbs: List[DBInitData] = []
    for index in range(lenadbs):
        temp_dict = DBInitData(
            user=safe_list_get(users, index, ""),
            password=safe_list_get(passwords, index, ""),
            host=safe_list_get(hosts, index, ""),
            port=safe_list_get(ports, index, ""),
            database=safe_list_get(databases, index, ""),
        )
        available_dbs.append(temp_dict)

    return available_dbs


class Connection:
    def __init__(self) -> None:
        self.__available_dbs = getDBInfo()

    def connect(self, _db: int = 0) -> connection:
        try:
            _connection = connect(
                **self.__available_dbs[_db], connection_factory=LoggingConnection
            )
            _connection.initialize(logging.getLogger("db_logger"))
            return _connection
        except psycopg2.OperationalError as exc:
            raise psycopg2.OperationalError(
                "No fue posible realizar una conexion"
            ) from exc

    @contextmanager
    def _open_connection(
        self, db: int = 0, *, dict_conn: Optional[bool] = None
    ) -> Generator[connection, None, None]:
        try:
            _connection = connect(
                **self.__available_dbs[db],
                connection_factory=(
                    LoggingConnection if not dict_conn else LoggingRealDictConnection
                ),
            )
            _connection.initialize(logging.getLogger("db_logger"))
        except psycopg2.OperationalError as exc:
            raise psycopg2.OperationalError(
                "No fue posible realizar una conexion"
            ) from exc
        else:
            try:
                with _connection as conn:
                    yield conn
            finally:
                _connection.close()

    def closeConnection(self, _connection: connection):
        _connection.close()
