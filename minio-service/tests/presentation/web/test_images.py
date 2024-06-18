from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    'data', [{
        'filename': 'test.png'
    }]
)
async def test_create_image(
        data: dict[str, str],
        app_client: AsyncClient,
        get_img: str
) -> None:
    with open(get_img, 'rb') as file:
        response = await app_client.post(
            '/images',
            data=data,
            files=[('image', file)]
        )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'url' in data


@pytest.mark.parametrize(
    'data', [{
        'filename': 'test.png'
    }]
)
async def test_update_image(
        data: dict[str, str],
        app_client: AsyncClient,
        get_img: str
) -> None:
    with open(get_img, 'rb') as file:
        response = await app_client.put(
            '/images',
            data=data,
            files=[('image', file)]
        )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'data', [{
        'filename': 'test.png'
    }]
)
async def test_delete_image(
        data: dict[str, str],
        app_client: AsyncClient
) -> None:
    response = await app_client.delete(
        f'/images/{data["filename"]}'
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
