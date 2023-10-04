from app.api.routes import router as api_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def get_application():
    app = FastAPI(title="Phresh Marketplace", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()


@app.get("/")
def home_page():
    return {"detail": "Home page not found"}
