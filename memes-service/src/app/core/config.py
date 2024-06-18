import os
from dataclasses import dataclass

from .exceptions import ConfigParseError


@dataclass
class PostgresConfig:
    db_url: str


@dataclass
class MinioServiceConfig:
    url: str


def get_str_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ConfigParseError(f'{key} is not set')
    return value


def load_postgres_config() -> PostgresConfig:
    return PostgresConfig(db_url=get_str_env('DB_URI'))


def load_minio_service_config() -> MinioServiceConfig:
    return MinioServiceConfig(url=get_str_env('MINIO_SERVICE'))
