from dataclasses import dataclass

from multidict import CIMultiDictProxy
from pydantic import BaseSettings, Field

from .conftest import query_es_create_films_documents


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


class TestSettings(BaseSettings):
    es_host: str = Field('elasticsearch:9200', env='ELASTIC_HOST')
    # service_url: str = Field('http://movie_api:8000', env='SERVICE_URL')
    service_url: str = Field('http://127.0.0.1:8001', env='SERVICE_URL')
    query_body: str = Field(None, env='TEST_QUERY')


test_settings = TestSettings(query_body=query_es_create_films_documents)
es_host = test_settings.es_host
service_url = test_settings.service_url
query_body = test_settings.query_body

