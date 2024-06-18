from minio_app.domain.models.image import ResultImageDTO


class ImageService:
    def get_url(self, url: str) -> ResultImageDTO:
        return ResultImageDTO(url=url)
