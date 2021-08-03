from fastapi import Request


def get_params(request: Request) -> dict:
    """
    Формируем из параметров запроса словарь.
    """
    search_params = dict(request.query_params.multi_items()) if request.query_params else None
    if search_params:
        search_params.pop('page', None) # Удаляем параметр пагинации page
    return search_params