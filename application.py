from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from core.config import get_settings


def get_application():
    _app = FastAPI(
        title=get_settings().PROJECT_NAME,
        # openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
        dependencies=[Depends(get_settings)],
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

if __name__ == "__main__":
    uvicorn.run("application:application", debug=True)

