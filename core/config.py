from functools import lru_cache
from typing import Any, List, Optional, Union

from fastapi import Depends, FastAPI
from pydantic import AnyHttpUrl, Field, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

from schemas.tags import description, extra_info, tags_metadata


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ## DB
    POSTGRES_READ_SERVER: str
    POSTGRES_READ_PORT: int
    POSTGRES_READ_USER: str
    POSTGRES_READ_PASSWORD: str
    POSTGRES_READ_DB: str

    POSTGRES_WRITE_SERVER: str
    POSTGRES_WRITE_PORT: int
    POSTGRES_WRITE_USER: str
    POSTGRES_WRITE_PASSWORD: str
    POSTGRES_WRITE_DB: str

    SQLALCHEMY_DATABASE_READ_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_WRITE_URI: Optional[PostgresDsn] = None

    POOL_MAX_SIZE: int = Field(..., gt=0)
    POOL_MIN_SIZE: int = Field(..., ge=0)
    POOL_MAX_IDLE: int = Field(..., ge=0)

    @field_validator("SQLALCHEMY_DATABASE_READ_URI", mode="before")
    @classmethod
    def assemble_db_connection_read(
        cls, value: Optional[str], values: ValidationInfo
    ) -> Any:
        """Build postgres uri"""
        data: dict | str = values.data

        if isinstance(data, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            username=data.get("POSTGRES_READ_USER"),
            password=data.get("POSTGRES_READ_PASSWORD"),
            host=data.get("POSTGRES_READ_SERVER", ""),
            port=data.get("POSTGRES_READ_PORT", ""),
            path=f"{data.get('POSTGRES_READ_DB') or ''}",
        )

    @field_validator("SQLALCHEMY_DATABASE_WRITE_URI", mode="before")
    def assemble_db_connection_write(
        cls, value: Optional[str], values: ValidationInfo
    ) -> Any:
        """Build postgres uri"""
        data: dict | str = values.data

        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            username=data.get("POSTGRES_WRITE_USER"),
            password=data.get("POSTGRES_WRITE_PASSWORD"),
            host=data.get("POSTGRES_WRITE_SERVER", ""),
            port=data.get("POSTGRES_WRITE_PORT", ""),
            path=f"{data.get('POSTGRES_WRITE_DB') or ''}",
        )

    class Config:
        """Config class"""

        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Returns cached settings"""

    return Settings()  # type: ignore


_app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description=description,
    # openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
    dependencies=[Depends(get_settings)],
    openapi_tags=tags_metadata,
    terms_of_service=extra_info.get("repositorio", ""),
)
