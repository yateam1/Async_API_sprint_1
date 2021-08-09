import logging

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api.v1 import film, genre, person
from core import config
from core.config import PROJECT_HOST, PROJECT_PORT
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

add_pagination(app)


@app.on_event('startup')
async def startup():
    redis.redis = aioredis.from_url(f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}', encoding="utf8", decode_responses=True)
    elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    FastAPICache.init(RedisBackend(redis.redis), prefix="movie_api-cache")


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(film.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genre.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(person.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=PROJECT_HOST,
        port=PROJECT_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
        debug=True,
    )
