import os
from logging import config as logging_config

from pydantic import BaseModel

from core.logger import LOGGING


class ProjectSettings(BaseModel):
    name: str
    host: str
    port: int


class RedisSettings(BaseModel):
    host: str
    port: int


class ElasticSettings(BaseModel):
    host: str
    port: int


class Config(BaseModel):
    movie_api: ProjectSettings
    redis: RedisSettings
    elasticsearch: ElasticSettings


logging_config.dictConfig(LOGGING)  # Применяем настройки логирования

config = Config.parse_file('config.json')

# Настройки проекта
PROJECT_NAME = config.movie_api.name  # Название проекта. Используется в Swagger-документации
PROJECT_HOST = config.movie_api.host
PROJECT_PORT = config.movie_api.port
SAMPLE_SIZE = 100  # Размер выборки по умолчанию для запросов из эластика

# Настройки Redis
REDIS_HOST = config.redis.host
REDIS_PORT = config.redis.port

# Настройки Elasticsearch
ELASTIC_HOST = config.elasticsearch.host
ELASTIC_PORT = config.elasticsearch.port

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
