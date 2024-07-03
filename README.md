# Tutorial Service FastAPI
`зачетный проект для университета`

UI часть проекта написана на VueJS, найти можно [тут (link)](https://github.com/raison-collab/TutoringServiceFrontendVueJS)
## Installation dependences
* If you use Windows, then `pip install -r requirements.txt`
* If you use other system, then you need to install `psycopg2-binary`. For that `pip install -r requirements.txt`, `pip install psycopg2-binary`

## Setup
* В файле `.env.prod` 

  * Необходимо установить `FRONTEND_HOST` в формате IpV4 `0.0.0.0`
  * `FRONTEND_PORT` Установить такой же, как тот, на котором запускался контейнер с образом `tutoring-service-vue`. По умолчанию `5173`
* Запустить в докере. По умолчанию будет доступен по http://127.0.0.1:8887/docs

## Docker
### Для запуска отдельного сервиса из docker compose
`docker compose --env-file ENV_FILE up -d --build SERVICE_NAME`

### Рекомендуемый способ запуска

1. Создать сеть `docker network create services_network`
2. Запустить `docker-compose-main-service.yml` `docker compose -f .\docker-compose-main-services.yml up --build` Данным способом запускается postgresql и jenkins
3. Запустить `docker-compose.yaml` `docker compose up --build` Данным способ запустится fast-api

Для корректной работы jenkins должны быть созданы контейнеры `alembic_runner` и `fast-api-container`
