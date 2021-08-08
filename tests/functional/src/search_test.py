import aiohttp
import pytest
import json

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch


SERVICE_URL = 'http://127.0.0.1:8001'
BODY_STRING = '''{"index": {"_index": "movies", "_id": 0}}
{'title': 'Movie title: 16', 'description': 'Plot of movie 16', 'creation_date': '2021-08-04', 'rating': 9.0, 'type': 'movie', 'genres': ['Genre_17', 'Genre_3', 'Genre_7'], 'actors': ['Last name11 First name11', 'Last name13 First name13', 'Last name16 First name16', 'Last name22 First name22', 'Last name24 First name24'], 'writers': ['Last name13 First name13', 'Last name16 First name16', 'Last name22 First name22', 'Last name24 First name24', 'Last name4 First name4'], 'directors': ['Last name11 First name11', 'Last name13 First name13', 'Last name24 First name24', 'Last name29 First name29', 'Last name4 First name4']}
'''
KEY = ''

@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
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
        url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
          return HTTPResponse(
            body=await response.json(),
            headers=response.headers,
            status=response.status,
          )
    return inner


@pytest.mark.asyncio
async def test_search_detailed(es_client, make_get_request):
    # Заполнение данных для теста
    await es_client.bulk(body=json.dumps(BODY_STRING))

    # Выполнение запроса
    response = await make_get_request('/films?genre=Genre 1')

    # Проверка результата
    assert response.status == 200
    assert response.body['id'] == 'fc258fa6-886f-4997-a498-556a8f208ac2'

    # Выполнение запроса
    response = await make_get_request('/films?genre=Genre 1&person=Person 1')

    # Проверка результата
    assert response.status == 200
    assert response.body['id'] == 'fc258fa6-886f-4997-a498-556a8f208ac2'

    # Выполнение запроса
    response = await make_get_request('/films?size=50')

    # Проверка результата
    assert response.status == 200
    assert response.body['total'] == 50