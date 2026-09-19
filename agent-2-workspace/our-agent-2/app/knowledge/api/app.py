from fastapi import FastAPI

from app.knowledge.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Enterprise Knowledge Agent",
        version="1.0.0",
    )

    app.include_router(router)

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    return app


app = create_app()
