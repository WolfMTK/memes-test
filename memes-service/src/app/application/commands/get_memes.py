from dataclasses import dataclass

from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.dto import Pagination
from app.application.protocols.interactor import Interactor
from app.application.protocols.uow import UoW
from app.domain.models.meme import MemeResultDTO
from app.domain.services.meme import MemeService


@dataclass
class GetMemesListsDTO:
    pagination: Pagination


@dataclass
class MemesListsResultDTO:
    total: int
    limit: int
    offset: int
    memes: list[MemeResultDTO]


class GetMemes(Interactor[GetMemesListsDTO, MemesListsResultDTO]):
    def __init__(
            self,
            uow: UoW,
            meme_gateway: StubDatabaseMemeGateway,
            service: MemeService
    ) -> None:
        self.uow = uow
        self.meme_gateway = meme_gateway
        self.service = service

    async def __call__(self, data: GetMemesListsDTO) -> MemesListsResultDTO:
        total_memes = await self.meme_gateway.get_total_memes()
        memes = self.meme_gateway.get_all(
            limit=data.pagination.limit,
            offset=data.pagination.offset
        )
        memes = await self.service.get_memes(memes)  # type: ignore
        return MemesListsResultDTO(
            total=total_memes,
            limit=data.pagination.limit,
            offset=data.pagination.offset,
            memes=memes
        )
