from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    Form,
    File,
    status,
)

from minio_app.application.delete_image import DeleteImageDTO
from minio_app.domain.models.image import ResultImageDTO, NewImageDTO
from minio_app.presentation.image_interactor import ImageInteractorFactory

image_router = APIRouter(prefix='/images', tags=['images'])


@image_router.post('', response_model=ResultImageDTO)
async def create_image(
        image: UploadFile,
        filename: str = Form(),
        ioc: ImageInteractorFactory = Depends()
):
    async with ioc.create_image() as create_image_factory:
        return await create_image_factory(
            NewImageDTO(image.file, filename)
        )


@image_router.put('')
async def update_image(
        image: UploadFile = File(default=None),
        filename: str = Form(default=None),
        ioc: ImageInteractorFactory = Depends()
):
    async with ioc.update_image() as update_image_factory:
        return await update_image_factory(
            NewImageDTO(image.file, filename)
        )


@image_router.delete(
    '/{filename}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_image(
        filename: str,
        ioc: ImageInteractorFactory = Depends()
) -> None:
    async with ioc.delete_image() as delete_image_factory:
        return await delete_image_factory(
            DeleteImageDTO(filename)
        )
