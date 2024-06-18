from http import HTTPStatus
from typing import Any
from urllib.parse import urljoin

import aiohttp

from app.adapter.exceptions import InvalidCodeError
from app.application.protocols.request import AbstractAioHTTPRequest


class AioHTTPRequest(AbstractAioHTTPRequest):
    def __init__(self, url: str) -> None:
        self.url = url

    async def upload_file(
            self,
            url: str,
            **kwargs: Any
    ) -> dict[str, Any]:
        url = urljoin(self.url, url)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=kwargs) as response:
                if response.status in (HTTPStatus.BAD_REQUEST,
                                       HTTPStatus.INTERNAL_SERVER_ERROR):
                    raise InvalidCodeError('Oops! Something went wrong')
                return await response.json()

    async def update_file(
            self,
            url: str,
            **kwargs: Any
    ) -> dict[str, Any]:
        url = urljoin(self.url, url)
        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=kwargs) as response:
                if response.status in (HTTPStatus.BAD_REQUEST,
                                       HTTPStatus.INTERNAL_SERVER_ERROR):
                    raise InvalidCodeError('Oops! Something went wrong')
                return await response.json()

    async def delete_file(
            self,
            url: str,
            **kwargs: Any
    ) -> None:
        url = urljoin(self.url + '/', url)
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                if response.status in (HTTPStatus.BAD_REQUEST,
                                       HTTPStatus.INTERNAL_SERVER_ERROR):
                    raise InvalidCodeError('Oops! Something went wrong')
