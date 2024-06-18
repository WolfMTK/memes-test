import uuid
from collections.abc import AsyncGenerator
from typing import Any

from app.core.contants import VALID_TYPES
from app.domain.exceptions import InvalidFileExtension, NotFoundURLException, MemeNotFoundException
from app.domain.models.meme import Meme, MemeResultDTO


class MemeService:
    def create_meme(self, text: str, image: str, url_image: str) -> Meme:
        # сделал генерацию uuid на стороне бэка
        return Meme(
            id=uuid.uuid4(),
            text=text,
            image=image,
            url_image=url_image
        )

    def check_content_type(self, filename: str) -> None:
        file_extension = filename.split('.')
        if file_extension[-1].upper() not in VALID_TYPES:
            raise InvalidFileExtension()

    def get_url_image(self, data: dict[str, Any]) -> str:
        url = data.get('url')
        if url is None:
            raise NotFoundURLException('Oops! Something went wrong')
        return url

    def get_filename(self, meme: Meme) -> str:
        url = meme.url_image
        if url is None:
            raise NotFoundURLException('Oops! Something went wrong')
        return url.split('/')[-1]

    def check_meme(self, meme: Meme) -> None:
        if meme is None:
            raise MemeNotFoundException()

    def get_meme(self, meme: Meme) -> MemeResultDTO:
        return MemeResultDTO(
            id=meme.id,
            text=meme.text,
            urlImage=meme.url_image
        )

    async def get_memes(self, memes: AsyncGenerator[Meme, Any]) -> list[MemeResultDTO]:
        return [MemeResultDTO(
            id=meme.id,
            text=meme.text,
            urlImage=meme.url_image
        ) async for meme in memes]
