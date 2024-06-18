import uuid
from dataclasses import dataclass


@dataclass
class BaseMeme:
    id: uuid.UUID | None
    text: str


@dataclass(kw_only=True)
class Meme(BaseMeme):
    url_image: str
    image: str


@dataclass(kw_only=True)
class MemeResultDTO(BaseMeme):
    urlImage: str


@dataclass
class MemeText:
    text: str
