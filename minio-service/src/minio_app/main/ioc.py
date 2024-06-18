from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends

from minio_app.application.create_image import CreateImage
from minio_app.application.delete_image import DeleteImage
from minio_app.application.protocols.minio_client import AbstractMinioClient
from minio_app.application.update_image import UpdateImage
from minio_app.domain.service.image import ImageService
from minio_app.presentation.image_interactor import ImageInteractorFactory


class ImageIOC(ImageInteractorFactory):
    def __init__(
            self,
            minio_client: AbstractMinioClient = Depends()
    ) -> None:
        self.minio_client = minio_client
        self.image_service = ImageService()

    @asynccontextmanager
    async def create_image(self) -> AsyncIterator[CreateImage]:
        yield CreateImage(
            self.minio_client,
            self.image_service
        )

    @asynccontextmanager
    async def update_image(self) -> AsyncIterator[UpdateImage]:
        yield UpdateImage(
            self.minio_client,
            self.image_service
        )

    @asynccontextmanager
    async def delete_image(self) -> AsyncIterator[DeleteImage]:
        yield DeleteImage(
            self.minio_client
        )
