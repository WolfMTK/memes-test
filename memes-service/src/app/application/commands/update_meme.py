import uuid
from dataclasses import dataclass, field

from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.protocols.interactor import Interactor
from app.application.protocols.request import AbstractAioHTTPRequest
from app.application.protocols.uow import UoW
from app.domain.services.meme import MemeService


@dataclass
class UpdateMemeDTO:
    id: uuid.UUID
    text: str | None = field(default=None)
    image: bytes | None = field(default=None)


class UpdateMeme(Interactor[UpdateMemeDTO, None]):
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

    async def __call__(self, data: UpdateMemeDTO) -> None:
        meme = await self.meme_gateway.get(id=data.id)
        self.meme_service.check_meme(meme)
        filename = self.meme_service.get_filename(meme)
        await self.request.update_file(
            '',
            image=data.image,
            filename=filename
        )
        await self.meme_gateway.update(meme.id, text=data.text)
        await self.uow.commit()
