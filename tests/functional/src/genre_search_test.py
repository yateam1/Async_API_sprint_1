import pytest

from ..conftest import query_es_create_genres_documents


@pytest.mark.asyncio
async def test_make_genres_fixtures(es_client):
    await es_client.bulk(body=query_es_create_genres_documents)


@pytest.mark.asyncio
async def test_search_genres_by_name(event_loop, make_get_request):
    response = await make_get_request('/genres?query=Genre 1')


@pytest.mark.asyncio
async def test_search_genres_by_wrong_name(event_loop, make_get_request):
    response = await make_get_request('/genres?query=asd')


@pytest.mark.asyncio
async def test_search_genres_with_size_1(event_loop, make_get_request):
    response = await make_get_request('/genres?size=1')
    assert response.body['total'] == 1
    assert len(response.body['items']) == 1


@pytest.mark.asyncio
async def test_search_genres_with_size_2(event_loop, make_get_request):
    response = await make_get_request('/genres?size=2')
    assert response.body['total'] == 2
    assert len(response.body['items']) == 2


@pytest.mark.asyncio
async def test_search_genres_with_size_1_and_from_1(event_loop, make_get_request):
    response = await make_get_request('/genres?size=1&from=1')
    assert response.body['total'] == 1
    assert len(response.body['items']) == 1
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb4'
    assert response.body['items'][0]['name'] == 'Genre 2'


@pytest.mark.asyncio
async def test_search_genres_with_size_1_and_from_2(event_loop, make_get_request):
    response = await make_get_request('/genres?size=1&from=2')
    assert response.body['total'] == 1
    assert len(response.body['items']) == 1
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb5'
    assert response.body['items'][0]['name'] == 'Genre 3'


@pytest.mark.asyncio
async def test_search_genres_with_size_1_and_from_3(event_loop, make_get_request):
    response = await make_get_request('/genres?size=1&from=3')
    assert response.body['total'] == 0
    assert len(response.body['items']) == 0


@pytest.mark.asyncio
async def test_search_genres_with_size_2_and_from_1(event_loop, make_get_request):
    response = await make_get_request('/genres?size=2&from=1')
    assert response.body['total'] == 2
    assert len(response.body['items']) == 2
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb4'
    assert response.body['items'][0]['name'] == 'Genre 2'
    assert response.body['items'][1]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb5'
    assert response.body['items'][1]['name'] == 'Genre 3'


@pytest.mark.asyncio
async def test_search_genres_with_size_2_and_from_2(event_loop, make_get_request):
    response = await make_get_request('/genres?size=2&from=2')
    assert response.body['total'] == 1
    assert len(response.body['items']) == 1
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb5'
    assert response.body['items'][0]['name'] == 'Genre 3'


@pytest.mark.asyncio
async def test_search_genres_with_size_2_and_from_3(event_loop, make_get_request):
    response = await make_get_request('/genres?size=2&from=3')
    assert response.body['total'] == 0
    assert len(response.body['items']) == 0
