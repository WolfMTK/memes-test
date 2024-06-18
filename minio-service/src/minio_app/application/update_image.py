from minio_app.application.protocols.interactor import Interactor
from minio_app.application.protocols.minio_client import AbstractMinioClient
from minio_app.domain.models.image import ResultImageDTO, NewImageDTO
from minio_app.domain.service.image import ImageService


class UpdateImage(Interactor[NewImageDTO, ResultImageDTO]):
    def __init__(
            self,
            minio_client: AbstractMinioClient,
            image_service: ImageService
    ) -> None:
        self.minio_client = minio_client
        self.image_service = image_service

    async def __call__(self, data: NewImageDTO) -> ResultImageDTO:
        self.minio_client.update_file(
            self.minio_client.bucket_name,
            data.filename,
            data.image
        )
        return self.image_service.get_url(self.minio_client.url)
