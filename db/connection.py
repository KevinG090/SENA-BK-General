""" Connection to db basics """

from typing import TypeVar, Generic

from pydantic import BaseModel

from psycopg_pool import (
    ConnectionPool,
    AsyncConnectionPool,
    AsyncNullConnectionPool,
    NullConnectionPool,
)

from core.config import get_settings
from application import application


T = TypeVar("T", ConnectionPool, AsyncConnectionPool)


class DBInstanceType(BaseModel, Generic[T]):
    """Get db connections"""

    read: T
    write: T

    class Config:
        """Config db generators"""

        arbitrary_types_allowed = True


class DBPoolDispatcher(BaseModel):
    """Get db conections"""

    sync_pool: DBInstanceType[NullConnectionPool]
    async_pool: DBInstanceType[AsyncNullConnectionPool]


pool_dispatcher = DBPoolDispatcher(
    sync_pool=DBInstanceType[NullConnectionPool](
        read=NullConnectionPool(
            get_settings().SQLALCHEMY_DATABASE_READ_URI or "",
            open=False,
            max_size=get_settings().POOL_MAX_SIZE,
            name="sync-read-pool",
        ),
        write=NullConnectionPool(
            get_settings().SQLALCHEMY_DATABASE_WRITE_URI or "",
            open=False,
            max_size=get_settings().POOL_MAX_SIZE,
            name="sync-write-pool",
        ),
    ),
    async_pool=DBInstanceType[AsyncNullConnectionPool](
        read=AsyncNullConnectionPool(
            get_settings().SQLALCHEMY_DATABASE_READ_URI or "",
            open=False,
            max_size=get_settings().POOL_MAX_SIZE,
            name="async-read-pool",
        ),
        write=AsyncNullConnectionPool(
            get_settings().SQLALCHEMY_DATABASE_WRITE_URI or "",
            open=False,
            max_size=get_settings().POOL_MAX_SIZE,
            name="async-write-pool",
        ),
    ),
)


@application.on_event("startup")
async def open_pool():
    """function to open db pool when application starts"""

    pool_dispatcher.sync_pool.read.open()
    pool_dispatcher.sync_pool.write.open()
    await pool_dispatcher.async_pool.read.open()
    await pool_dispatcher.async_pool.write.open()


@application.on_event("shutdown")
async def close_pool():
    """function to close db pool when application shutdowns"""

    pool_dispatcher.sync_pool.read.close()
    pool_dispatcher.sync_pool.write.close()
    await pool_dispatcher.async_pool.read.close()
    await pool_dispatcher.async_pool.write.close()
