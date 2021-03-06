import pytest

from ..conftest import query_es_create_films_documents


@pytest.mark.asyncio
async def test_make_films_fixtures(es_client):
    await es_client.bulk(body=query_es_create_films_documents)


@pytest.mark.asyncio
async def test_search_films_by_name(make_get_request):
    await make_get_request('/films?query=Movie 2')


@pytest.mark.asyncio
async def test_search_films_by_wrong_name(make_get_request):
    await make_get_request('/films?query=asd')


@pytest.mark.asyncio
async def test_search_films_with_size_1(make_get_request):
    response = await make_get_request('/films?size=1')

    assert response.body['total'] == 1
    assert len(response.body['items']) == 1


@pytest.mark.asyncio
async def test_search_films_with_size_2(make_get_request):
    response = await make_get_request('/films?size=2')

    assert response.body['total'] == 2
    assert len(response.body['items']) == 2


@pytest.mark.asyncio
async def test_search_films_with_size_1_and_from_1(make_get_request):
    response = await make_get_request('/films?size=1&from=1')

    assert response.body['total'] == 1
    assert len(response.body['items']) == 1
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb4'
    assert response.body['items'][0]['title'] == 'Movie title: 17'


@pytest.mark.asyncio
async def test_search_films_with_size_1_and_from_2(make_get_request):
    response = await make_get_request('/films?size=1&from=2')

    assert response.body['total'] == 1
    assert len(response.body['items']) == 1
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb5'
    assert response.body['items'][0]['title'] == 'Movie title: 18'


@pytest.mark.asyncio
async def test_search_films_with_size_1_and_from_3(make_get_request):
    response = await make_get_request('/films?size=1&from=3')

    assert response.body['total'] == 1
    assert len(response.body['items']) == 1
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb6'
    assert response.body['items'][0]['title'] == 'Movie title: 19'


@pytest.mark.asyncio
async def test_search_films_with_size_2_and_from_1(make_get_request):
    response = await make_get_request('/films?size=2&from=1')

    assert response.body['total'] == 2
    assert len(response.body['items']) == 2
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb4'
    assert response.body['items'][0]['title'] == 'Movie title: 17'
    assert response.body['items'][1]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb5'
    assert response.body['items'][1]['title'] == 'Movie title: 18'


@pytest.mark.asyncio
async def test_search_films_with_size_2_and_from_2(make_get_request):
    response = await make_get_request('/films?size=2&from=2')

    assert response.body['total'] == 2
    assert len(response.body['items']) == 2
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb5'
    assert response.body['items'][0]['title'] == 'Movie title: 18'
    assert response.body['items'][1]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb6'
    assert response.body['items'][1]['title'] == 'Movie title: 19'


@pytest.mark.asyncio
async def test_search_films_with_size_2_and_from_3(make_get_request):
    response = await make_get_request('/films?size=2&from=3')

    assert response.body['total'] == 2
    assert len(response.body['items']) == 2
    assert response.body['items'][0]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb6'
    assert response.body['items'][0]['title'] == 'Movie title: 19'
    assert response.body['items'][1]['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb7'
    assert response.body['items'][1]['title'] == 'Movie title: 20'
