from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    'data', [{
        'text': 'test'
    }]
)
async def test_create_meme(
        data: dict[str, str],
        app_client: AsyncClient,
        get_img: str
) -> None:
    pass
    with open(get_img, 'rb') as file:
        response = await app_client.post(
            '/memes',
            data=data,
            files=[('image', file)]
        )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert 'id' in data


@pytest.mark.parametrize(
    'data', [{
        'text': 'test'
    }]
)
async def test_invali_file_create_meme(
        data: dict[str, str],
        app_client: AsyncClient,
        get_pdf: str
) -> None:
    with open(get_pdf, 'rb') as file:
        response = await app_client.post(
            '/memes',
            data=data,
            files=[('image', file)]
        )
    assert response.status_code != HTTPStatus.CREATED


async def test_empty_data_create_meme(app_client: AsyncClient):
    response = await app_client.post('/memes')
    assert response.status_code != HTTPStatus.CREATED


async def test_get_memes(app_client: AsyncClient) -> None:
    response = await app_client.get('/memes')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    keys = ('total', 'limit', 'offset', 'memes')
    assert sorted(data) == sorted(keys)
    memes = data['memes']
    assert isinstance(memes, list)
    assert len(memes) != 0


@pytest.mark.parametrize(
    'data', [{
        'text': 'test'
    }]
)
async def test_get_meme(
        data: dict[str, str],
        app_client: AsyncClient,
        get_img: str
) -> None:
    with open(get_img, 'rb') as file:
        response = await app_client.post(
            '/memes',
            data=data,
            files=[('image', file)]
        )
    assert response.status_code == HTTPStatus.CREATED
    meme_id = response.json().get('id')
    response = await app_client.get(f'/memes/{meme_id}')
    keys = ('id', 'text', 'urlImage')
    data = response.json()
    assert sorted(data) == sorted(keys)


@pytest.mark.parametrize(
    'data', [
        {
            'text': 'test2'
        }
    ]
)
async def test_update_meme(
        data: dict[str, str],
        app_client: AsyncClient,
        get_img: str
) -> None:
    with open(get_img, 'rb') as file:
        response = await app_client.post(
            '/memes',
            data=data,
            files=[('image', file)]
        )
    assert response.status_code == HTTPStatus.CREATED
    meme_id = response.json().get('id')
    response = await app_client.put(f'/memes/{meme_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.parametrize(
    'data', [
        {
            'text': 'test'
        }
    ]
)
async def delete_meme(
        data: dict[str, str],
        app_client: AsyncClient,
        get_img: str
) -> None:
    with open(get_img, 'rb') as file:
        response = await app_client.post(
            '/memes',
            data=data,
            files=[('image', file)]
        )
    assert response.status_code == HTTPStatus.CREATED
    meme_id = response.json().get('id')
    response = await app_client.delete(f'/memes/{meme_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT
