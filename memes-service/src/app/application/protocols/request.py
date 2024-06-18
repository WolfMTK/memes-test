from abc import ABC, abstractmethod
from typing import Any


class AbstractAioHTTPRequest(ABC):
    @abstractmethod
    async def upload_file(
            self,
            url: str,
            **kwargs: Any
    ) -> dict[str, Any]: ...

    @abstractmethod
    async def update_file(
            self,
            url: str,
            **kwargs: Any
    ) -> dict[str, Any]: ...

    @abstractmethod
    async def delete_file(
            self,
            url: str,
            **kwargs: Any
    ) -> None: ...
