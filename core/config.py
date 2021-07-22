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
    project: ProjectSettings
    redis: RedisSettings
    elastic: ElasticSettings


logging_config.dictConfig(LOGGING)  # Применяем настройки логирования

config = Config.parse_file('config.json')

# Настройки проекта
PROJECT_NAME = config.project.name  # Название проекта. Используется в Swagger-документации
PROJECT_HOST = config.project.host
PROJECT_PORT = config.project.port

# Настройки Redis
REDIS_HOST = config.redis.host
REDIS_PORT = config.redis.port

# Настройки Elasticsearch
ELASTIC_HOST = config.elastic.host
ELASTIC_PORT = config.elastic.port

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
