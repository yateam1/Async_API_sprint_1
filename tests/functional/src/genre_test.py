import pytest

@pytest.mark.asyncio
async def test_get_genre(event_loop, make_get_request):

    response = await make_get_request('/genres/unknown')

    assert response.status == 404
    assert response.body['detail'] == 'genre not found'

@pytest.mark.asyncio
async def test_get_genres_data(event_loop, make_get_request):

    response = await make_get_request('/genres')

    assert response.status == 200
    assert response.body['total'] == 3
    assert response.body['page'] == 1
    assert response.body['size'] == 50
    assert len(response.body['items']) == 3

@pytest.mark.asyncio
async def test_get_genre_data_by_id(event_loop, make_get_request, validateGenresJSON):

    response = await make_get_request('/genres/ead9b449-734b-4878-86f1-1e4c96a28bb3')

    assert response.status == 200
    assert validateGenresJSON(response.body) == True
    assert response.body['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb3'
    assert response.body['name'] == 'Genre 1'

    response = await make_get_request('/genres/ead9b449-734b-4878-86f1-1e4c96a28bb4')

    assert response.status == 200
    assert validateGenresJSON(response.body) == True
    assert response.body['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb4'
    assert response.body['name'] == 'Genre 2'

    response = await make_get_request('/genres/ead9b449-734b-4878-86f1-1e4c96a28bb5')

    assert response.status == 200
    assert validateGenresJSON(response.body) == True
    assert response.body['id'] == 'ead9b449-734b-4878-86f1-1e4c96a28bb5'
    assert response.body['name'] == 'Genre 3'

@pytest.mark.asyncio
async def test_get_genre_data_by_unknown_id(event_loop, make_get_request):

    response = await make_get_request('/genres/ead9b449-734b-4878-86f1-1e4c96a28bba')

    assert response.status == 404
    assert response.body['detail'] == 'Not found'

    response = await make_get_request('/genres/random_id')

    assert response.status == 404
    assert response.body['detail'] == 'Not found'