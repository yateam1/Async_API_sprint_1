# Запуск проекта

Проект запускается в Docker-контейнерах вместе со связанными приложениями

### Перед запуском контейнеров нужно файл .env.dist скопировать в .env.
В файле указать следующие переменные:
- DJANGO_SECRET_KEY=<секретный ключ Django>
- POSTGRES_DB=movies
- POSTGRES_USER=movies
- POSTGRES_PASSWORD=<укажите ваш пароль>

### Команды для запуска приложений:
Для запуска в режиме разработки
```bash
docker-compose build
```
```bash
docker-compose up -d
```

Для запуска в production
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

Тестирование проекта
```bash
cd tests/functional
docker-compose build
docker-compose up
```


### Заполнение базы данных фикстурами
1. С помощью команды ```docker ps``` узнайте имя контейнера c приложением admin_panel
2. Войдите в контейнер и запустите консоль django shell командой ```docker exec -it <имя контейнера> ./manage.py shell```
4. Внутри консоли выполните команды:
```
from movie.factories import make_objects
make_objects()
```

### Заполнение индексов ElasticSearch
После запуска docker-compose индексы ElasticSearch (movies, genres, persons) создадутся и запонятся автоматически в течении 4-х минут.
Для ручного обновления индексов необходимо:
1. С помощью команды ```docker ps``` узнайте имя контейнера, в котором запущен redis
2. Войдите в контейнер ```docker exec -it <имя контейнера> redis-cli```
3. Удалите ключ, который содержит дату предыдущего обновления индексов, командой ```# del Movie_ETL [movies]```
После этих действий индексы обновятся полностью (т.е. будет запрос на все записи базы данных).

Далее обновление индексов передёт в штатный режим - через каждые три минуты.

### Примеры использования сервиса
1. Получение всех фильмов с пагинацией [127.0.0.1/api/v1/film?page=2](127.0.0.1/api/v1/film?page=2)
2. Получение информации о персоне по uuid [127.0.0.1/api/v1/person/uuid](127.0.0.1/api/v1/person/02ca6d8d-a96e-4890-a113-5f145acd45b1)
3. Получение всей схемы сервиса [127.0.0.1/api/opeapi](127.0.0.1/api/opeapi)