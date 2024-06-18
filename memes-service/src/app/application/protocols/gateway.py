import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Any

BaseModel = TypeVar('BaseModel')


class CreatedGateway(ABC):
    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> BaseModel: ...


class ReadingGateway(ABC):
    @abstractmethod
    async def get(self, *args: Any, **kwargs: Any) -> BaseModel | None: ...


class UpdatingGateway(ABC):
    @abstractmethod
    async def update(
            self,
            id: uuid.UUID,
            *args: Any, **kwargs: Any
    ) -> BaseModel: ...


class DeletedGateway(ABC):
    @abstractmethod
    async def delete(self, *args: Any, **kwargs: Any) -> None: ...
