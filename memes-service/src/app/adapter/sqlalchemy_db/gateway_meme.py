from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.adapter.sqlalchemy_db.models import Meme
from app.adapter.stub_db_meme import StubDatabaseMemeGateway


class MemeGateway(StubDatabaseMemeGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, **kwargs: Any) -> Meme:
        stmt = insert(Meme).values(**kwargs).returning(Meme)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(
            self,
            limit: int,
            offset: int,
            **kwargs: Any
    ) -> AsyncGenerator[Meme, Any]:
        stmt = select(Meme).filter_by(**kwargs).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        # я бы сразу возвращал массив, но решил через генератор делать
        for val in result.scalars():
            yield val

    async def get(self, **kwargs: Any) -> Meme | None:
        stmt = select(Meme).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, id: int, **kwargs: Any) -> Meme:
        kwargs = {
            key: value for key, value in kwargs.items() if value is not None
        }
        if not kwargs:
            return await self.get(id=id)
        stmt = update(Meme).where(
            Meme.id == id
        ).values(**kwargs).returning(Meme)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, **kwargs: Any) -> None:
        stmt = delete(Meme).filter_by(**kwargs)
        await self.session.execute(stmt)

    async def get_total_memes(self) -> int:
        stmt = select(func.count(Meme.id))
        return await self.session.scalar(stmt)
