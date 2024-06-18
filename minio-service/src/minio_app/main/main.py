from fastapi import FastAPI

from minio_app.adapter import init_dependencies
from minio_app.application.protocols.minio_client import AbstractMinioClient
from minio_app.presentation.image_interactor import ImageInteractorFactory
from minio_app.presentation.web import image_router
from .ioc import ImageIOC


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url=None, redoc_url=None
    )
    app.include_router(image_router)
    init_dependencies(app)
    app.dependency_overrides.update(
        {
            ImageInteractorFactory: ImageIOC
        }
    )

    @app.on_event('startup')
    async def create_bucket():
        minio_client: AbstractMinioClient = app.dependency_overrides[
            AbstractMinioClient
        ]()
        if not minio_client.check_bucket(minio_client.bucket_name):
            minio_client.create_bucket(minio_client.bucket_name)
            minio_client.set_policy(minio_client.bucket_name)

    return app
