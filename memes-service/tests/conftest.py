import os
import uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from app.adapter.stub_db_meme import StubDatabaseMemeGateway
from app.application.protocols.request import AbstractAioHTTPRequest
from app.application.protocols.uow import UoW
from app.domain.models.meme import Meme
from app.main import create_app as create_fastapi_app

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DB_NAME = 'test.db'
FILES_NAME = ['test.png', 'test.pdf']
DIR_DB = BASE_DIR / DB_NAME


@pytest.fixture
def get_img() -> str:
    filename = FILES_NAME[0]
    base_dir = BASE_DIR / filename
    with open(base_dir, encoding='utf-8', mode='w') as file:
        file.close()
    return str(base_dir)


@pytest.fixture
def get_pdf() -> str:
    filename = FILES_NAME[1]
    base_dir = BASE_DIR / filename
    with open(base_dir, encoding='utf-8', mode='w') as file:
        file.close()
    return str(base_dir)


class TestAioHTTPRequest(AbstractAioHTTPRequest):
    def __init__(self, url: str) -> None:
        self.url = url

    async def upload_file(
            self,
            url: str,
            **kwargs: Any
    ) -> dict[str, Any]:
        return {'url': 'http://test.ru/12.png'}

    async def update_file(
            self,
            url: str,
            **kwargs: Any
    ) -> dict[str, Any]:
        return {'url': 'http://test.ru/12.png'}

    async def delete_file(
            self,
            url: str,
            **kwargs: Any
    ) -> None:
        return None


class TestGateway(StubDatabaseMemeGateway):
    def __init__(self):
        self._meme_id: uuid.UUID = '0a83c17d-dad9-416e-aca6-4cc39c0e2c43'
        self._len_memes = 10

    async def create(self, **kwargs: Any) -> Meme:
        return Meme(
            id=self._meme_id,
            text='test',
            url_image=f'http://test/{FILES_NAME[0]}',
            image=FILES_NAME[0]
        )

    async def get_all(self, **kwargs: Any) -> AsyncGenerator[Meme, Any]:
        memes = (
            Meme(
                id=self._meme_id,
                text='test',
                url_image=f'http://test/{FILES_NAME[0]}',
                image=FILES_NAME[0]
            ) for _ in range(self._len_memes)
        )
        for val in memes:
            yield val

    async def get(self, **kwargs: Any) -> Meme | None:
        return Meme(
            id=self._meme_id,
            text='test',
            url_image=f'http://test/{FILES_NAME[0]}',
            image=FILES_NAME[0]
        )

    async def update(self, id: uuid.uuid4(), **kwargs: Any) -> Meme:
        meme = Meme(
            id=self._meme_id,
            text='test',
            url_image=f'http://test/{FILES_NAME[0]}',
            image=FILES_NAME[0]
        )
        for key, value in kwargs.items():
            setattr(meme, key, value)
        return meme

    async def delete(self, **kwargs: Any) -> None:
        pass

    async def get_total_memes(self) -> int:
        return self._len_memes


def new_request(url: str) -> TestAioHTTPRequest:
    return TestAioHTTPRequest(url)


def new_gateway() -> TestGateway:
    yield TestGateway()


@dataclass
class TestConfig:
    db_url: str = 'sqlite+aiosqlite:///test.db'
    url: str = 'service'


def load_config() -> dict[str, Any]:
    return {
        'DB_URI': TestConfig.db_url,
        'MINIO_SERVICE': TestConfig.url
    }


@pytest.fixture
def set_environ() -> None:
    for key, value in load_config().items():
        os.environ[key] = value


@pytest.fixture
async def mock_uow() -> UoW:
    uow = AsyncMock()
    uow.commit = AsyncMock()
    uow.flush = AsyncMock()
    uow.rollback = AsyncMock()
    return uow


@pytest.fixture
async def app_client(
        set_environ: None,
        mock_uow: UoW
) -> None:
    app = create_fastapi_app()
    app.dependency_overrides[UoW] = lambda: mock_uow
    app.dependency_overrides[StubDatabaseMemeGateway] = new_gateway
    app.dependency_overrides[AbstractAioHTTPRequest] = (
        lambda: new_request('http://test.ru')
    )
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
