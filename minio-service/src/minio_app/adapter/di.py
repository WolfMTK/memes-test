from fastapi import FastAPI

from minio_app.adapter.minio_client import MinioClient
from minio_app.application.protocols.minio_client import AbstractMinioClient
from minio_app.core import load_minio_config


def new_minio_client(
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool,
        bucket_name: str
) -> MinioClient:
    return MinioClient(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure,
        bucket_name=bucket_name
    )


def init_dependencies(app: FastAPI) -> None:
    minio_config = load_minio_config()
    app.dependency_overrides.update(
        {
            AbstractMinioClient: lambda: new_minio_client(
                endpoint=minio_config.endpoint,
                access_key=minio_config.access_key,
                secret_key=minio_config.secret_key,
                secure=minio_config.secure,
                bucket_name=minio_config.bucket_name
            )
        }
    )
