import os

from environs import Env
from logging import config as logging_config

from core.logger import LOGGING

env = Env()
env.read_env()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = env.str('PROJECT_NAME', 'movies')
PROJECT_HOST = env.str('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = env.int('PROJECT_PORT', 8000)

# Настройки Redis
REDIS_HOST = env.str('REDIS_HOST', '127.0.0.1')
REDIS_PORT = env.int('REDIS_PORT', 6379)

# Настройки Elasticsearch
ELASTIC_HOST = env.str('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = env.int('ELASTIC_PORT', 9200)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
