import uuid
from dataclasses import dataclass, asdict

from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.protocols.interactor import Interactor
from app.application.protocols.request import AbstractAioHTTPRequest
from app.application.protocols.uow import UoW
from app.domain.services.meme import MemeService


@dataclass
class NewMemeDTO:
    text: str
    image: bytes
    filename: str


@dataclass
class MemeIDDTO:
    id: uuid.UUID


class CreateMeme(Interactor[NewMemeDTO, MemeIDDTO]):
    def __init__(
            self,
            uow: UoW,
            meme_gateway: StubDatabaseMemeGateway,
            meme_service: MemeService,
            request: AbstractAioHTTPRequest
    ) -> None:
        self.uow = uow
        self.meme_gateway = meme_gateway
        self.meme_service = meme_service
        self.request = request

    async def __call__(self, data: NewMemeDTO) -> MemeIDDTO:
        self.meme_service.check_content_type(data.filename)
        url = self.meme_service.get_url_image(
            await self.request.upload_file(
                '',
                image=data.image,
                filename=data.filename
            )
        )
        meme = self.meme_service.create_meme(
            text=data.text,
            image=data.filename,
            url_image=url
        )
        meme = await self.meme_gateway.create(**asdict(meme))
        meme_id = meme.id
        await self.uow.commit()
        return MemeIDDTO(id=meme_id)
