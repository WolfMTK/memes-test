from fastapi import FastAPI

from app import adapter
from app.presentation.meme_interactor import MemeInteractorFactory
from app.presentation.web import meme_router
from .ioc import MemeIOC


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(meme_router)
    adapter.init_dependency(app)
    app.dependency_overrides.update(
        {
            MemeInteractorFactory: MemeIOC
        }
    )
    return app
