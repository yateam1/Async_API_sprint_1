import orjson
from pydantic import BaseModel, Field

from models.base import orjson_dumps


class APIParams(BaseModel):
    """Базовая модель параметров урла приложения"""
    from_: int = Field(0, alias='from') # пагинация "с"
    size_: int = Field(10, alias='size') # пагинация "сколько"
    query_: str = Field('', alias='query') # поисковая строка

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        
        extra = 'forbid'
        