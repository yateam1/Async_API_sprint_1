import pytest
from ..conftest import query_es_create_persons_documents

@pytest.mark.asyncio
async def test_make_persons_fixtures(es_client):
    await es_client.bulk(body=query_es_create_persons_documents)

@pytest.mark.asyncio
async def test_get_person(make_get_request):

    response = await make_get_request('/persons/unknown', expected_status_code=404)
    assert response.body['detail'] == 'person not found'

@pytest.mark.asyncio
async def test_get_persons_data(make_get_request):

    response = await make_get_request('/persons')
    assert response.body['total'] == 5
    assert response.body['page'] == 1
    assert response.body['size'] == 50
    assert len(response.body['items']) == 5

@pytest.mark.asyncio
async def test_get_person_data_by_id(make_get_request, validatePersonsJSON):
    response = await make_get_request('/persons/ead9b449-734b-4878-86f1-1e4c96a28bb3')
    assert validatePersonsJSON(response.body) == True
    assert response.body['birth_date'] == '2021-08-05'
    assert response.body['first_name'] == 'First name4'
    assert response.body['last_name'] == 'Last name4'
    assert response.body['writer'] == []
    assert response.body['actor'] == ['02365fab-bfdf-4f3b-8282-862d990ef293', '02365fab-bfdf-4f3b-8282-862d990ef294']
    assert response.body['director'] == ['02365fab-bfdf-4f3b-8282-862d990ef293', '02365fab-bfdf-4f3b-8282-862d990ef294']
    assert response.body['producer'] == ['02365fab-bfdf-4f3b-8282-862d990ef293', '02365fab-bfdf-4f3b-8282-862d990ef294']

@pytest.mark.asyncio
async def test_get_person_data_by_unknown_id(make_get_request):

    response = await make_get_request('/persons/ead9b449-734b-4878-86f1-1e4c96a28bba', expected_status_code=404)
    assert response.body['detail'] == 'person not found'

    response = await make_get_request('/persons/random_id', expected_status_code=404)
    assert response.body['detail'] == 'person not found'
