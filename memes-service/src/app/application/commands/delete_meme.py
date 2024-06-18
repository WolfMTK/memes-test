import uuid

from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.protocols.interactor import Interactor
from app.application.protocols.request import AbstractAioHTTPRequest
from app.application.protocols.uow import UoW
from app.domain.services.meme import MemeService


class DeleteMeme(Interactor[uuid.UUID, None]):
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

    async def __call__(self, meme_id: uuid.UUID) -> None:
        meme = await self.meme_gateway.get(id=meme_id)
        self.meme_service.check_meme(meme)
        filename = self.meme_service.get_filename(meme)
        await self.request.delete_file(url=filename)
        await self.meme_gateway.delete(id=meme_id)
        await self.uow.commit()
