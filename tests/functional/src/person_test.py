import json

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from ..settings import query_body, HTTPResponse, service_url, es_host


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=es_host)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = service_url + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
          return HTTPResponse(
            body=await response.json(),
            headers=response.headers,
            status=response.status,
          )
    return inner


@pytest.mark.asyncio
async def test_person_search(es_client, make_get_request):
    # Заполнение данных для теста
    await es_client.bulk(body=query_body)

    # Выполнение запроса
    response = await make_get_request('/persons/fc258fa6-886f-4997-a498-556a8f208ac2')

    # Проверка результата
    assert response.status == 200
    assert response.body['id'] == 'fc258fa6-886f-4997-a498-556a8f208ac2'

    response = await make_get_request('/persons')

    # Проверка результата
    assert response.status == 200
    assert response.body['total'] == 95