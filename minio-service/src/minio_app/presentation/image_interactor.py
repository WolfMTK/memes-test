from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from minio_app.application.create_image import CreateImage
from minio_app.application.delete_image import DeleteImage
from minio_app.application.update_image import UpdateImage


class ImageInteractorFactory(ABC):
    @abstractmethod
    def create_image(self) -> AbstractAsyncContextManager[CreateImage]: ...

    @abstractmethod
    def update_image(self) -> AbstractAsyncContextManager[UpdateImage]: ...

    @abstractmethod
    def delete_image(self) -> AbstractAsyncContextManager[DeleteImage]: ...
