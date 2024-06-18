import os
from dataclasses import dataclass

from .exceptions import ConfigParseError


@dataclass
class MinioConfig:
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool
    bucket_name: str


def get_str_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ConfigParseError(f'{key} is not set')
    return value


def load_minio_config() -> MinioConfig:
    return MinioConfig(
        endpoint=get_str_env('MINIO_ENDPOINT'),
        access_key=get_str_env('MINIO_ACCESS_KEY'),
        secret_key=get_str_env('MINIO_SECRET_KEY'),
        secure=True if get_str_env(
            'MINIO_SECURE'
        ) in ('true', 'True') else False,
        bucket_name=get_str_env('MINIO_BUCKET_NAME')
    )
