from abc import ABC, abstractmethod
from typing import BinaryIO


class AbstractMinioClient(ABC):
    @property
    @abstractmethod
    def bucket_name(self) -> str: ...

    @property
    @abstractmethod
    def path(self) -> str: ...

    @property
    @abstractmethod
    def url(self) -> str: ...

    @abstractmethod
    def check_bucket(self, name: str) -> bool: ...

    @abstractmethod
    def create_bucket(self, name: str) -> None: ...

    @abstractmethod
    def set_policy(self, name: str) -> None: ...

    @abstractmethod
    def send_file(
            self,
            bucket_name: str,
            object_name: str,
            file: BinaryIO
    ) -> None: ...

    @abstractmethod
    def update_file(
            self,
            bucket_name: str,
            object_name: str,
            file: BinaryIO
    ) -> None: ...

    @abstractmethod
    def delete_file(self, bucket_name: str, object_name: str) -> None: ...
