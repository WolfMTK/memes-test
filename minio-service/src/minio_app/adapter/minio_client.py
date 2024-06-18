import json
import os
import uuid
from typing import BinaryIO
from urllib.parse import urljoin, urlparse

from minio import Minio

from minio_app.application.protocols.minio_client import AbstractMinioClient

_CONTENT_TYPE = {
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'jpg': 'image/jpg'
}


class MinioClient(AbstractMinioClient):
    _path: str | None = None

    def __init__(
            self,
            endpoint: str,
            access_key: str,
            secret_key: str,
            secure: bool,
            bucket_name: str
    ) -> None:
        self._url = urlparse(endpoint)
        self._bucket_name = bucket_name
        self._client = Minio(
            self._url.netloc,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def path(self) -> str | None:
        return self._path

    @property
    def url(self) -> str:
        # можно было взять от Starlette структуру с URL,
        # но решил, что не стоит
        url = self._parse_url()
        if self.path is None:
            return url
        return urljoin(url, self.path)

    def send_file(
            self,
            bucket_name: str,
            object_name: str,
            file: BinaryIO
    ) -> None:
        object_name = object_name.split('.')

        object_extension = object_name[-1]
        object_name = f'{self._random_filename()}.{object_extension}'
        self._send_file(
            bucket_name,
            object_name,
            file,
            object_extension
        )
        self._path = f'{bucket_name}/{object_name}'

    def update_file(
            self,
            bucket_name: str,
            object_name: str | None,
            file: BinaryIO | None
    ) -> None:
        if object_name is None and file is None:
            return
        object_extension = object_name.split('.')[-1]
        # сделал через обновление объекта, но, наверно, лучше
        # было бы через создание нового объекта в S3
        self._send_file(
            bucket_name,
            object_name,
            file,
            object_extension
        )
        self._path = f'{bucket_name}/{object_name}'

    def delete_file(self, bucket_name: str, object_name: str) -> None:
        self._client.remove_object(
            bucket_name=bucket_name,
            object_name=object_name
        )

    def _send_file(
            self,
            bucket_name: str,
            object_name: str,
            file: BinaryIO,
            object_extension: str
    ):
        try:
            self._client.put_object(
                bucket_name,
                object_name,
                file,
                os.fstat(file.fileno()).st_size,
                content_type=self._get_content_type(
                    object_extension.lower()
                )
            )
        except Exception as err:
            # Minio doesn't throw a specific error
            raise AttributeError from err

    def check_bucket(self, name: str) -> bool:
        return self._client.bucket_exists(name)

    def create_bucket(self, name: str) -> None:
        self._client.make_bucket(name)

    def set_policy(self, name: str) -> None:
        policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Principal': {'AWS': '*'},
                    'Action': ['s3:GetBucketLocation', 's3:ListBucket'],
                    'Resource': f'arn:aws:s3:::{name}',
                },
                {
                    'Effect': 'Allow',
                    'Principal': {'AWS': '*'},
                    'Action': 's3:GetObject',
                    'Resource': f'arn:aws:s3:::{name}/*',
                },
            ],
        }
        self._client.set_bucket_policy(name, json.dumps(policy))

    def _get_content_type(self, key: str) -> str:
        try:
            return _CONTENT_TYPE[key]
        except KeyError as err:
            raise AssertionError from err

    def _random_filename(self) -> str:
        return str(uuid.uuid4())

    def _parse_url(self) -> str:
        scheme = self._url.scheme
        netloc = self._url.netloc
        return f'{scheme}://{netloc}'
