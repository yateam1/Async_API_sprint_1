FROM python:3.9.5

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
