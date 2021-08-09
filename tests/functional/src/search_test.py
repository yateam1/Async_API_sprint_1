import json

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from ..settings import query_body, HTTPResponse, service_url, es_host
from ..utils.utils import es_client, session, make_get_request


@pytest.mark.asyncio
async def test_search_detailed(es_client, make_get_request):
    # Заполнение данных для теста
    await es_client.bulk(body=query_body)

    # Выполнение запроса
    response = await make_get_request('/genres?name=Genre 1')

    # Проверка результата
    assert response.status == 200

    # Выполнение запроса
    response = await make_get_request('/films?query=Movie 2')

    # Проверка результата
    assert response.status == 200

    # Выполнение запроса
    response = await make_get_request('/films?size=50')

    # Проверка результата
    assert response.status == 200
    assert response.body['total'] > 0