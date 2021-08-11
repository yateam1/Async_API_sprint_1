import pytest
import aiohttp
import asyncio

from elasticsearch import AsyncElasticsearch

from ..settings import query_body, HTTPResponse, service_url, es_host
from ..conftest import query_es_create_films_documents, query_es_create_genres_documents, query_es_create_persons_documents


# @pytest.yield_fixture
# def event_loop():
#     """Create an instance of the default event loop for each test case."""
#     policy = asyncio.get_event_loop_policy()
#     res = policy.new_event_loop()
#     asyncio.set_event_loop(res)
#     res._close = res.close
#     res.close = lambda: None

#     yield res

#     res._close()

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


@pytest.fixture(scope='session')
async def es_bulk_items_add(es_client):
    await es_client.bulk(body=query_es_create_films_documents)
    await es_client.bulk(body=query_es_create_genres_documents)
    await es_client.bulk(body=query_es_create_persons_documents)


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = service_url + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
