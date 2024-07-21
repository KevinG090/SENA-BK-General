from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyHttpUrl, Field, PostgresDsn, ValidationInfo, field_validator
from pydantic_core import MultiHostHost
from pydantic_settings import BaseSettings

from libs.exception_handler import init_handlers
from schemas.tags import description, extra_info, tags_metadata


class Settings(BaseSettings):
    """Configuracion y captura de variables de entorno"""

    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            if not v.startswith("["):
                return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):  # type: ignore
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

    POSTGRES_URL_TEMP: str

    SQLALCHEMY_DATABASE_READ_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_WRITE_URI: Optional[PostgresDsn] = None

    POOL_MAX_SIZE: int = Field(..., gt=0)
    POOL_MIN_SIZE: int = Field(..., ge=0)
    POOL_MAX_IDLE: int = Field(..., ge=0)

    APP_LLAVE_AES_ENCRYPT: str
    APP_IV_AES_ENCRYPT: str

    @field_validator("SQLALCHEMY_DATABASE_READ_URI", mode="before")
    def assemble_db_connection_read(
        cls, value: Optional[str], values: ValidationInfo
    ) -> Union[MultiHostHost, str]:
        """Build postgres uri"""
        data: Dict[str, Any] = values.data  # type: ignore

        if isinstance(value, str):
            return value
        return PostgresDsn.build(  # type: ignore
            scheme="postgres",
            username=data.get("POSTGRES_READ_USER"),
            password=data.get("POSTGRES_READ_PASSWORD"),
            host=data.get("POSTGRES_READ_SERVER", ""),
            port=data.get("POSTGRES_READ_PORT"),
            path=f"{data.get('POSTGRES_READ_DB') or ''}",
        )

    @field_validator("SQLALCHEMY_DATABASE_WRITE_URI", mode="before")
    def assemble_db_connection_write(
        cls, value: Optional[str], values: ValidationInfo
    ) -> Union[MultiHostHost, str]:
        """Build postgres uri"""
        data: Dict[str, Any] = values.data  # type: ignore

        if isinstance(value, str):
            return value
        return PostgresDsn.build(  # type: ignore
            scheme="postgres",
            username=data.get("POSTGRES_WRITE_USER"),
            password=data.get("POSTGRES_WRITE_PASSWORD"),
            host=data.get("POSTGRES_WRITE_SERVER", ""),
            port=data.get("POSTGRES_WRITE_PORT"),
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


# Configuracion del entorno
app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description=description,
    # openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
    dependencies=[Depends(get_settings)],
    openapi_tags=tags_metadata,
    terms_of_service=extra_info.get("repositorio", ""),
)


def get_application():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


application = get_application()

init_handlers(application)
