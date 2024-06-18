from dataclasses import dataclass

from minio_app.application.protocols.interactor import Interactor
from minio_app.application.protocols.minio_client import AbstractMinioClient


@dataclass
class DeleteImageDTO:
    filename: str


class DeleteImage(Interactor[DeleteImageDTO, None]):
    def __init__(
            self,
            minio_client: AbstractMinioClient,
    ) -> None:
        self.minio_client = minio_client

    async def __call__(self, data: DeleteImageDTO) -> None:
        self.minio_client.delete_file(
            self.minio_client.bucket_name,
            data.filename
        )
