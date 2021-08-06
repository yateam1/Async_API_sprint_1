FROM python:3.9.5

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]