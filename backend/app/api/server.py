from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import config
from app.db.tasks import close_db_connection, connect_to_db


PREFIX_URL = "/api"


def get_application():
    app = FastAPI(
        title=config.project_name,
        version=config.project_version,
        docs_url=f"{PREFIX_URL}/docs",
        openapi_url=f"{PREFIX_URL}/apidoc.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=PREFIX_URL)
    return app


app = get_application()


@app.on_event("startup")
async def startup_event():
    await connect_to_db()


@app.on_event("shutdown")
async def startup_event():
    await close_db_connection()


@app.get("/")
def home_page():
    return {"detail": "Home page"}
