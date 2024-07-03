# Tutorial Service FastAPI
`зачетный проект для университета`

UI часть проекта написана на VueJS, найти можно [тут (link)](https://github.com/raison-collab/TutoringServiceFrontendVueJS)
## Installation dependences
* If you use Windows, then `pip install -r requirements.txt`
* If you use other system, then you need to install `psycopg2-binary`. For that `pip install -r requirements.txt`, `pip install psycopg2-binary`


## env example

```dotenv
DB_HOST=postgres-container
DB_PORT=5432
DB_NAME=tutoring_service_database
DB_PASSWORD=postgres
DB_USER=postgres
DB_CONNECTION_TIMES=10

TOKEN_SECRET_KEY=secret

SERVER_HOST=127.0.0.1
SERVER_PORT=8060
SERVER_PROTOCOL=http

DEBUG=False

FRONTEND_HOST=127.0.0.1
FRONTEND_PORT=5173
FRONTEND_PROTOCOL=http
```

## Setup
* Создать `.env.prod` и заполнить как в разделе `env example` выше
* В файле `.env.prod` 

  * Необходимо установить `FRONTEND_HOST` в формате IpV4 `0.0.0.0`
  * `FRONTEND_PORT` Установить такой же, как тот, на котором запускался контейнер с образом `tutoring-service-vue`. По умолчанию `5173`
* Запустить в докере. По умолчанию будет доступен по http://127.0.0.1:8887/docs

## Docker

`docker compose up -d --build`

### Для запуска отдельного сервиса из docker compose
`docker compose --env-file ENV_FILE up -d --build SERVICE_NAME`