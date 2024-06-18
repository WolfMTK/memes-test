import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO

import pytest
from httpx import AsyncClient

from minio_app.application.protocols.minio_client import AbstractMinioClient
from minio_app.main import create_app as create_fastapi_app

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
IMAGE_NAME = 'test.png'


class TestMinioClient(AbstractMinioClient):
    def __init__(self):
        self._bucket_name = 'images'

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def path(self) -> str:
        return f'{self._bucket_name}/file.png'

    @property
    def url(self) -> str:
        return f'https://localhost:9000/{self.path}'

    def check_bucket(self, name: str) -> bool:
        return True

    def create_bucket(self, name: str) -> None:
        pass

    def set_policy(self, name: str) -> None:
        pass

    def send_file(
            self,
            bucket_name: str,
            object_name: str,
            file: BinaryIO
    ) -> None:
        pass

    def update_file(
            self,
            bucket_name: str,
            object_name: str,
            file: BinaryIO
    ) -> None:
        pass

    def delete_file(self, bucket_name: str, object_name: str) -> None:
        pass


def new_minio_client() -> TestMinioClient:
    return TestMinioClient()


@pytest.fixture
def get_img() -> str:
    filename = IMAGE_NAME
    base_dir = BASE_DIR / filename
    with open(base_dir, encoding='utf-8', mode='w') as file:
        file.close()
    return str(base_dir)


@dataclass
class TestConfig:
    endpoint: str = 'endpoint'
    access_key: str = 'access-key'
    secret_key: str = 'secret-key'
    secure: str = 'True'
    bucket_name: str = 'bucket_name'


def load_config() -> dict[str, Any]:
    return {
        'MINIO_ENDPOINT': TestConfig.endpoint,
        'MINIO_ACCESS_KEY': TestConfig.access_key,
        'MINIO_SECRET_KEY': TestConfig.secret_key,
        'MINIO_SECURE': TestConfig.secure,
        'MINIO_BUCKET_NAME': TestConfig.bucket_name
    }


@pytest.fixture
def set_environ() -> None:
    for key, value in load_config().items():
        os.environ[key] = value


@pytest.fixture
async def app_client(set_environ: None) -> None:
    app = create_fastapi_app()
    app.dependency_overrides[AbstractMinioClient] = new_minio_client
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
