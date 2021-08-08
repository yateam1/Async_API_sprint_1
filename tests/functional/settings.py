from pydantic import BaseSettings, Field

class TestSettings(BaseSettings):
    es_host: str = Field('elasticsearch:9200', env='ELASTIC_HOST')