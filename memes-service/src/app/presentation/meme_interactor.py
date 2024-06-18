from abc import abstractmethod, ABC
from contextlib import AbstractAsyncContextManager

from app.application.commands.create_meme import CreateMeme
from app.application.commands.delete_meme import DeleteMeme
from app.application.commands.get_meme import GetMeme
from app.application.commands.get_memes import GetMemes
from app.application.commands.update_meme import UpdateMeme


class MemeInteractorFactory(ABC):
    @abstractmethod
    def create_meme(self) -> AbstractAsyncContextManager[CreateMeme]: ...

    @abstractmethod
    def get_meme(self) -> AbstractAsyncContextManager[GetMeme]: ...

    @abstractmethod
    def get_memes(self) -> AbstractAsyncContextManager[GetMemes]: ...

    @abstractmethod
    def delete_meme(self) -> AbstractAsyncContextManager[DeleteMeme]: ...

    @abstractmethod
    def update_meme(self) -> AbstractAsyncContextManager[UpdateMeme]: ...
