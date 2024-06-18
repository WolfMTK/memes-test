from abc import abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from app.adapter.sqlalchemy_db.models import Meme
from app.application.protocols.gateway import (
    CreatedGateway,
    ReadingGateway,
    UpdatingGateway,
    DeletedGateway,
)


class StubDatabaseMemeGateway(
    CreatedGateway,
    ReadingGateway,
    UpdatingGateway,
    DeletedGateway
):
    @abstractmethod
    async def get_all(
            self,
            *args: Any,
            **kwargs: Any
    ) -> AsyncGenerator[Meme, Any]: ...

    @abstractmethod
    async def get_total_memes(self) -> int: ...
