from dataclasses import dataclass

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy
from pydantic import BaseSettings, Field

class TestSettings(BaseSettings):
    es_host: str = Field('elasticsearch:9200', env='ELASTIC_HOST')


SERVICE_URL = 'http://127.0.0.1:8001'
BODY_STRING = '''{"index": {"_index": "movies", "_id": 0}}
{'title': 'Movie title: 16', 'description': 'Plot of movie 16', 'creation_date': '2021-08-04', 'rating': 9.0, 'type': 'movie', 'genres': ['Genre_17', 'Genre_3', 'Genre_7'], 'actors': ['Last name11 First name11', 'Last name13 First name13', 'Last name16 First name16', 'Last name22 First name22', 'Last name24 First name24'], 'writers': ['Last name13 First name13', 'Last name16 First name16', 'Last name22 First name22', 'Last name24 First name24', 'Last name4 First name4'], 'directors': ['Last name11 First name11', 'Last name13 First name13', 'Last name24 First name24', 'Last name29 First name29', 'Last name4 First name4']}
'''
KEY = ''


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int
