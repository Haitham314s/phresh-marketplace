from app.api.routes import router as api_router
from app.core.config import config
from app.core.tasks import create_start_app_handler, create_stop_app_handler
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def get_application():
    app = FastAPI(title=config.project_name, version=config.project_version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", create_start_app_handler)
    app.add_event_handler("shutdown", create_stop_app_handler)

    app.include_router(api_router, prefix="/api")
    return app


app = get_application()


@app.get("/")
def home_page():
    return {"detail": "Home page"}
