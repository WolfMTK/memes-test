import uuid

from fastapi import (
    APIRouter,
    Depends,
    Form,
    UploadFile,
    HTTPException,
    status,
    File,
    Query,
)

from app.adapter.exceptions import InvalidCodeError
from app.application.commands.create_meme import NewMemeDTO, MemeIDDTO
from app.application.commands.get_memes import (
    GetMemesListsDTO,
    MemesListsResultDTO,
)
from app.application.commands.update_meme import UpdateMemeDTO
from app.application.dto import Pagination
from app.domain.exceptions import (
    InvalidFileExtension,
    NotFoundURLException,
    MemeNotFoundException,
)
from app.domain.models.meme import MemeResultDTO
from app.presentation.meme_interactor import MemeInteractorFactory
from app.presentation.openapi import (
    EXAMPLE_CREATE_MEME_RESPONSE,
    EXAMPLE_GET_MEMES_RESPONSE,
    EXAMPLE_UPDATE_MEME_RESPONSE,
    EXAMPLE_GET_MEME_RESPONSE,
    EXAMPLE_DELETE_MEME_RESPONSE,
)

meme_router = APIRouter(prefix='/memes', tags=['Memes'])


@meme_router.post(
    '',
    response_model=MemeIDDTO,
    status_code=status.HTTP_201_CREATED,
    responses=EXAMPLE_CREATE_MEME_RESPONSE
)
async def create_meme(
        image: UploadFile = File(description='Загрузка изображения мема'),
        text: str = Form(description='Описание мема'),
        ioc: MemeInteractorFactory = Depends()
):
    """
    Создание мема

    * **image** - изображение мема (обязательное поле)

    * **text** - описание мема (обязательное поле)
    """
    try:
        async with ioc.create_meme() as create_meme_factory:
            return await create_meme_factory(
                NewMemeDTO(
                    text=text,
                    image=image.file.read(),
                    filename=image.filename,
                )
            )
    except (InvalidCodeError,
            InvalidFileExtension,
            NotFoundURLException) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@meme_router.get(
    '',
    response_model=MemesListsResultDTO,
    responses=EXAMPLE_GET_MEMES_RESPONSE
)
async def get_memes(
        ioc: MemeInteractorFactory = Depends(),
        limit: int = Query(
            10, description='Ограничение на количество записей'
        ),
        offset: int = Query(0, description='Текущая страница')
):
    """Получение мемов"""
    async with ioc.get_memes() as get_memes_factory:
        return await get_memes_factory(
            (GetMemesListsDTO(Pagination(limit=limit, offset=offset)))
        )


@meme_router.get(
    '/{id}',
    response_model=MemeResultDTO,
    responses=EXAMPLE_GET_MEME_RESPONSE
)
async def get_meme(
        id: uuid.UUID,
        ioc: MemeInteractorFactory = Depends()
):
    """
    Получение мема

    * **id** - уникальный идентификатор мема
    """
    try:
        async with ioc.get_meme() as get_meme_factory:
            return await get_meme_factory(id)
    except MemeNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@meme_router.put(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses=EXAMPLE_UPDATE_MEME_RESPONSE
)
async def update_meme(
        id: uuid.UUID,
        image: UploadFile = File(
            default=None,
            description='Загрузка изображения мема'
        ),
        text: str = Form(
            default=None,
            description='Описание мема'
        ),
        ioc: MemeInteractorFactory = Depends()
) -> None:
    """
    Обновление мема

    * **id** - уникальный идентификатор мема

    * **image** - изображение мема

    * **text** - описание мема
    """
    if image is not None:
        image = image.file.read()
    try:
        async with ioc.update_meme() as update_meme_factory:
            return await update_meme_factory(
                UpdateMemeDTO(
                    id=id,
                    text=text,
                    image=image,
                )
            )
    except (InvalidCodeError, MemeNotFoundException) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@meme_router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses=EXAMPLE_DELETE_MEME_RESPONSE
)
async def delete_meme(
        id: uuid.UUID,
        ioc: MemeInteractorFactory = Depends()
):
    """
    Удаление мема

    * **id** - уникальный идентификатор мема
    """
    try:
        async with ioc.delete_meme() as delete_meme_factory:
            return await delete_meme_factory(id)
    except (InvalidCodeError, MemeNotFoundException) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
