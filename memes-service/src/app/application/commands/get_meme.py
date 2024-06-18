import uuid

from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.protocols.interactor import Interactor
from app.application.protocols.uow import UoW
from app.domain.models.meme import MemeResultDTO
from app.domain.services.meme import MemeService


class GetMeme(Interactor[uuid.UUID, MemeResultDTO]):
    def __init__(
            self,
            uow: UoW,
            meme_gateway: StubDatabaseMemeGateway,
            meme_service: MemeService
    ) -> None:
        self.uow = uow
        self.meme_gateway = meme_gateway
        self.meme_service = meme_service

    async def __call__(self, meme_id: uuid.UUID) -> MemeResultDTO:
        meme = await self.meme_gateway.get(id=meme_id)
        self.meme_service.check_meme(meme)
        meme = self.meme_service.get_meme(meme)
        return meme
