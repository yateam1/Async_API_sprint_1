# Запуск проекта

Проект запускается в Docker-контейнерах
## Вариант 1. Запуск только текущего приложения
Команды для запуска приложения:  
```$ docker-compose build```  
```$ docker-compose up -d```  

## Вариант 2. Запуск всех связанных приложений
Перед запуском контейнеров нужно файл .env.dist переименовать в .env.  
В файле указать следующие переменные:
- DJANGO_SECRET_KEY=<секретный ключ Django>

- POSTGRES_HOST=db
- POSTGRES_PORT=5432
- POSTGRES_DB=movies
- POSTGRES_USER=movies
- POSTGRES_PASSWORD=<укажите ваш пароль>
- REDIS_HOST=redis
- ELASTICSEARCH_HOST=elasticsearch

Команды для запуска приложений:  
```$ docker-compose -f docker-compose-full-project.yaml build```  
```$ docker-compose -f docker-compose-full-project.yaml up -d```  