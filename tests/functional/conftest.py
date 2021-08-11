query_es_create_films_documents = '''{"index": {"_index": "movies", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb3"}}
{"title": "Movie title: 16", "description": "Plot of movie 16", "creation_date": "2021-08-04", "rating": 9.0, "type": "movie", "genres": ["Genre_17", "Genre_3", "Genre_7"], "actors": ["Last name11 First name11", "Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24"], "writers": ["Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24", "Last name4 First name4"], "directors": ["Last name11 First name11", "Last name13 First name13", "Last name24 First name24", "Last name29 First name29", "Last name4 First name4"]}
{"index": {"_index": "movies", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb4"}}
{"title": "Movie title: 17", "description": "Plot of movie 17", "creation_date": "2021-08-04", "rating": 9.0, "type": "movie", "genres": ["Genre_17", "Genre_3", "Genre_7"], "actors": ["Last name11 First name11", "Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24"], "writers": ["Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24", "Last name4 First name4"], "directors": ["Last name11 First name11", "Last name13 First name13", "Last name24 First name24", "Last name29 First name29", "Last name4 First name4"]}
{"index": {"_index": "movies", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb5"}}
{"title": "Movie title: 18", "description": "Plot of movie 18", "creation_date": "2021-08-04", "rating": 9.0, "type": "movie", "genres": ["Genre_17", "Genre_3", "Genre_7"], "actors": ["Last name11 First name11", "Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24"], "writers": ["Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24", "Last name4 First name4"], "directors": ["Last name11 First name11", "Last name13 First name13", "Last name24 First name24", "Last name29 First name29", "Last name4 First name4"]}
{"index": {"_index": "movies", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb6"}}
{"title": "Movie title: 19", "description": "Plot of movie 19", "creation_date": "2021-08-04", "rating": 9.0, "type": "movie", "genres": ["Genre_17", "Genre_3", "Genre_7"], "actors": ["Last name11 First name11", "Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24"], "writers": ["Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24", "Last name4 First name4"], "directors": ["Last name11 First name11", "Last name13 First name13", "Last name24 First name24", "Last name29 First name29", "Last name4 First name4"]}
{"index": {"_index": "movies", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb7"}}
{"title": "Movie title: 20", "description": "Plot of movie 120", "creation_date": "2021-08-04", "rating": 9.0, "type": "movie", "genres": ["Genre_17", "Genre_3", "Genre_7"], "actors": ["Last name11 First name11", "Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24"], "writers": ["Last name13 First name13", "Last name16 First name16", "Last name22 First name22", "Last name24 First name24", "Last name4 First name4"], "directors": ["Last name11 First name11", "Last name13 First name13", "Last name24 First name24", "Last name29 First name29", "Last name4 First name4"]}
'''

query_es_create_genres_documents = '''
{"index": {"_index": "genres", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb3"}}
{"name":"Genre 1"}
{"index": {"_index": "genres", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb4"}}
{"name":"Genre 2"}
{"index": {"_index": "genres", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb5"}}
{"name":"Genre 3"}
'''

query_es_create_persons_documents = '''
{"index": {"_index": "persons", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb3"}}
{"actor":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"],  "birth_date": "2021-08-05", "director":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "first_name": "First name4",  "last_name": "Last name4", "producer":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "screenwriter":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"]}
{"index": {"_index": "persons", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb4"}}
{"actor":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"],  "birth_date": "2021-08-05", "director":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "first_name": "First name5",  "last_name": "Last name5", "producer":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "screenwriter":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"]}
{"index": {"_index": "persons", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb5"}}
{"actor":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"],  "birth_date": "2021-08-05", "director":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "first_name": "First name6",  "last_name": "Last name6", "producer":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "screenwriter":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"]}
{"index": {"_index": "persons", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb6"}}
{"actor":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"],  "birth_date": "2021-08-05", "director":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "first_name": "First name7",  "last_name": "Last name7", "producer":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "screenwriter":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"]}
{"index": {"_index": "persons", "_id": "ead9b449-734b-4878-86f1-1e4c96a28bb7"}}
{"actor":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"],  "birth_date": "2021-08-05", "director":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "first_name": "First name8",  "last_name": "Last name8", "producer":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"], "screenwriter":["02365fab-bfdf-4f3b-8282-862d990ef293", "02365fab-bfdf-4f3b-8282-862d990ef294"]}
'''

import pytest
import aiohttp
import asyncio
import json

from elasticsearch import AsyncElasticsearch

from .settings import query_body, HTTPResponse, service_url, es_host

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


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

@pytest.fixture(scope='session')
def validateFilmsJSON():
    def inner(jsonData):
        fields_list = (
            'actors',
            'creation_date',
            'description',
            'directors',
            'genres',
            'id',
            'producers',
            'rating',
            'title',
            'type',
            'writers',
        )
        return len(set(jsonData.keys()) - set(fields_list)) == 0
    return inner

@pytest.fixture(scope='session')
def validateGenresJSON():
    def inner(jsonData):
        fields_list = (
            'id',
            'name',
        )
        return len(set(jsonData.keys()) - set(fields_list)) == 0
    return inner

@pytest.fixture(scope='session')
def validatePersonsJSON():
    def inner(jsonData):
        fields_list = (
            'id',
            'actor',
            'birth_date',
            'director',
            'first_name',
            'last_name',
            'producer',
            'writer',
        )
        return len(set(jsonData.keys()) - set(fields_list)) == 0
    return inner