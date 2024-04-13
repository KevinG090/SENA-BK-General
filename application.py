""""""

import uvicorn

from app import api_router
from core.config import get_settings
from schemas.tags import (
    description,
    tags_metadata,
    extra_info,
)

from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware


def get_application():
    _app = FastAPI(
        title=get_settings().PROJECT_NAME,
        description=description,
        # openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
        dependencies=[Depends(get_settings)],
        openapi_tags= tags_metadata,
        terms_of_service = extra_info.get("repositorio","")
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app




application = get_application()

application.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("application:application", debug=True)

