from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


def orjson_dumps(v, *, default) -> str:
    """Ускоренная сериализация json.

    Pydantic требует unicode.
    """
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    """Базовая модель для всех моделей."""
    id: UUID = Field(default_factory=uuid4)

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
