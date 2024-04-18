""" Connection to db basics """

from typing import Any, Generic, TypeVar

from fastapi import Depends, FastAPI
from psycopg_pool import (
    AsyncConnectionPool,
    AsyncNullConnectionPool,
    ConnectionPool,
    NullConnectionPool,
)
from pydantic import BaseModel

from core.config import app as application
from core.config import get_settings

T = TypeVar("T", ConnectionPool, AsyncConnectionPool)


class DBInstanceType(BaseModel, Generic[T]):
    """Get db connections"""

    read: T
    write: T

    class Config:
        """Config db generators"""

        arbitrary_types_allowed = True


class DBPoolDispatcher(BaseModel):
    """Get db connections"""

    sync_pool: DBInstanceType[NullConnectionPool]
    async_pool: DBInstanceType[AsyncNullConnectionPool]


def create_connection_pool(uri: Any, max_size: int, name: str) -> Any:
    """Creates a connection pool based on type (sync or async)"""
    if isinstance(application, FastAPI):  # Assuming application is a FastAPI instance
        if "async" in name:  # Check if name suggests asynchronous pool
            return AsyncNullConnectionPool(
                str(uri).replace(" ", ""), open=False, max_size=max_size, name=name
            )
        else:
            return NullConnectionPool(
                str(uri).replace(" ", ""), open=False, max_size=max_size, name=name
            )
    else:
        raise ValueError("Application instance is not a FastAPI object")


pool_dispatcher = DBPoolDispatcher(
    sync_pool=DBInstanceType[NullConnectionPool](
        read=create_connection_pool(
            get_settings().SQLALCHEMY_DATABASE_READ_URI or "",
            get_settings().POOL_MAX_SIZE,
            "sync-read-pool",
        ),
        write=create_connection_pool(
            get_settings().SQLALCHEMY_DATABASE_WRITE_URI or "",
            get_settings().POOL_MAX_SIZE,
            "sync-write-pool",
        ),
    ),
    async_pool=DBInstanceType[AsyncNullConnectionPool](
        read=create_connection_pool(
            get_settings().SQLALCHEMY_DATABASE_READ_URI or "",
            get_settings().POOL_MAX_SIZE,
            "async-read-pool",
        ),
        write=create_connection_pool(
            get_settings().SQLALCHEMY_DATABASE_WRITE_URI or "",
            get_settings().POOL_MAX_SIZE,
            "async-write-pool",
        ),
    ),
)


async def open_pool(app: FastAPI = Depends(application)):
    """Function to open database pool when application starts"""

    if isinstance(application, FastAPI):  # Check if application is a FastAPI instance
        pool_dispatcher.sync_pool.read.open()
        pool_dispatcher.sync_pool.write.open()
        await pool_dispatcher.async_pool.read.open()
        await pool_dispatcher.async_pool.write.open()
    else:
        raise ValueError("Application instance is not a FastAPI object")


async def close_pool(app: FastAPI = Depends(application)):
    """Function to close database pool when application shutdowns"""

    if isinstance(application, FastAPI):  # Check if application is a FastAPI instance
        pool_dispatcher.sync_pool.read.close()
        pool_dispatcher.sync_pool.write.close()
        await pool_dispatcher.async_pool.read.close()
        await pool_dispatcher.async_pool.write.close()
    else:
        raise ValueError("Application instance is not a FastAPI object")


application.add_event_handler("startup", open_pool)
application.add_event_handler("shutdown", close_pool)
