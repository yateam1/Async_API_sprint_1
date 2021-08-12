import pytest

from ..conftest import query_es_create_films_documents

@pytest.mark.asyncio
async def test_make_films_fixtures(es_client):
    await es_client.bulk(body=query_es_create_films_documents)

@pytest.mark.asyncio
async def test_get_film(make_get_request):

    response = await make_get_request('/films/unknown', expected_status_code=404)
    assert response.body['detail'] == 'film not found'

@pytest.mark.asyncio
async def test_get_films_data(make_get_request):

    response = await make_get_request('/films')

    assert response.body['total'] == 5
    assert response.body['page'] == 1
    assert response.body['size'] == 50
    assert len(response.body['items']) == 5

@pytest.mark.asyncio
async def test_get_film_data_by_id(make_get_request, validateFilmsJSON):

    response = await make_get_request('/films/ead9b449-734b-4878-86f1-1e4c96a28bb7')
    assert validateFilmsJSON(response.body) == True
    assert response.body['creation_date'] == '2021-08-04'
    assert response.body['description'] == 'Plot of movie 120'
    assert response.body['title'] == 'Movie title: 20'
    assert response.body['type'] == 'movie'
    assert response.body['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb7'
    assert response.body['producers'] == []
    assert response.body['rating'] == float(9)
    assert response.body['writers'] == [
        'Last name13 First name13',
        'Last name16 First name16',
        'Last name22 First name22',
        'Last name24 First name24',
        'Last name4 First name4'
    ]
    assert response.body['actors'] == [
        "Last name11 First name11",
        "Last name13 First name13",
        "Last name16 First name16",
        "Last name22 First name22",
        "Last name24 First name24"
    ]
    assert response.body['directors'] == [
        "Last name11 First name11",
        "Last name13 First name13",
        "Last name24 First name24",
        "Last name29 First name29",
        "Last name4 First name4"
    ]

@pytest.mark.asyncio
async def test_get_film_data_by_unknown_id(make_get_request):

    response = await make_get_request('/films/ead9b449-734b-4878-86f1-1e4c96a28bba', expected_status_code=404)
    assert response.body['detail'] == 'film not found'
