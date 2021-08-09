import json

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from ..settings import query_body, HTTPResponse, service_url, es_host
from ..conftest import query_es_create_genres_documents
from ..utils.utils import es_client, session, make_get_request


@pytest.mark.asyncio
async def test_genre_search(es_client, make_get_request):
    # Заполнение данных для теста
    await es_client.bulk(body=query_es_create_genres_documents)

    # Выполнение запроса
    response = await make_get_request('/genres/unknown')

    # Проверка результата
    assert response.status == 404

    # Выполнение запроса
    response = await make_get_request('/genres')

    # Проверка результата
    assert response.status == 200
    assert response.body['total'] > 0

    # Выполнение запроса
    response = await make_get_request('/genres/ead9b449-734b-4878-86f1-1e4c96a28bb3')

    # Проверка результата
    assert response.status == 200