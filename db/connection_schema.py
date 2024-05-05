import logging
from contextlib import contextmanager
from typing import Generator, List, Optional, TypedDict, Union
from sqlalchemy.exc import SQLAlchemyError

from core.config import get_settings
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager



class Connection:
    def __init__(self) -> None:
        """"""

    def connect(self, _db: int = 0):
        try:
            uri = (
                get_settings().SQLALCHEMY_DATABASE_WRITE_URI
                if _db == 0
                else get_settings().SQLALCHEMY_DATABASE_READ_URI
            )
            engine = create_engine(str(uri))
            sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            _connection = sessionLocal()
            return _connection
        except SQLAlchemyError as exc:
            print(exc)
            raise SQLAlchemyError(
                "No fue posible realizar una conexion"
            ) from exc

    @contextmanager
    def _open_connection(
        self, db: int = 0, *, dict_conn: Optional[bool] = None
    ) :
        try:
            _connection = self.connect(db)
        except SQLAlchemyError as exc:
            raise SQLAlchemyError(
                "No fue posible realizar una conexion"
            ) from exc
        else:
            try:
                with _connection as conn:
                    yield conn
            finally:
                _connection.close()

    def closeConnection(self, _connection):
        _connection.close()
