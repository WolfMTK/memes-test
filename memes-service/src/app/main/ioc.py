from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import Depends

from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.commands.create_meme import CreateMeme
from app.application.commands.delete_meme import DeleteMeme
from app.application.commands.get_meme import GetMeme
from app.application.commands.get_memes import GetMemes
from app.application.protocols.request import AbstractAioHTTPRequest
from app.application.protocols.uow import UoW
from app.application.commands.update_meme import UpdateMeme
from app.domain.services.meme import MemeService
from app.presentation.meme_interactor import MemeInteractorFactory


class MemeIOC(MemeInteractorFactory):
    def __init__(
            self,
            uow: UoW = Depends(),
            meme_gateway: StubDatabaseMemeGateway = Depends(),
            request: AbstractAioHTTPRequest = Depends()
    ) -> None:
        self.uow = uow
        self.meme_gateway = meme_gateway
        self.service = MemeService()
        self.request = request

    @asynccontextmanager
    async def create_meme(self) -> AsyncIterator[CreateMeme]:
        yield CreateMeme(
            self.uow,
            self.meme_gateway,
            self.service,
            self.request
        )

    @asynccontextmanager
    async def get_meme(self) -> AsyncIterator[GetMeme]:
        yield GetMeme(
            self.uow,
            self.meme_gateway,
            self.service
        )

    @asynccontextmanager
    async def get_memes(self) -> AsyncIterator[GetMemes]:
        yield GetMemes(
            self.uow,
            self.meme_gateway,
            self.service
        )

    @asynccontextmanager
    async def delete_meme(self) -> AsyncIterator[DeleteMeme]:
        yield DeleteMeme(
            self.uow,
            self.meme_gateway,
            self.service,
            self.request
        )

    @asynccontextmanager
    async def update_meme(self) -> AsyncIterator[UpdateMeme]:
        yield UpdateMeme(
            self.uow,
            self.meme_gateway,
            self.service,
            self.request
        )
