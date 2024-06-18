from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class ResultImageDTO:
    url: str


@dataclass
class NewImageDTO:
    image: BinaryIO
    filename: str
