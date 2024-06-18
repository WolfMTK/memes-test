import functools
from collections.abc import Iterator

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapter import request_aiohttp
from app.adapter.sqlalchemy_db.connect import (
    create_async_session_maker,
    create_async_session,
)
from app.adapter.sqlalchemy_db.gateway_meme import MemeGateway
from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.protocols.request import AbstractAioHTTPRequest
from app.application.protocols.uow import UoW
from app.core import load_postgres_config, load_minio_service_config
from app.presentation.dependencies.di import Stub


def new_uow(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> AsyncSession:
    return session


def new_request(url: str) -> request_aiohttp.AioHTTPRequest:
    return request_aiohttp.AioHTTPRequest(url)


def new_meme_gateway(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> Iterator[MemeGateway]:
    yield MemeGateway(session)


def init_dependency(app: FastAPI) -> None:
    db_url = load_postgres_config().db_url
    session_maker = create_async_session_maker(db_url)
    minio_service_url = load_minio_service_config().url
    app.dependency_overrides.update(
        {
            AsyncSession: functools.partial(  # можно было через lamda сделать
                create_async_session,
                session_maker
            ),
            UoW: new_uow,
            StubDatabaseMemeGateway: new_meme_gateway,
            AbstractAioHTTPRequest: lambda: new_request(minio_service_url),
        }
    )
