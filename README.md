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

## возможные ошибки

* При запуске докера может показаться ошибка настройки переменных окружения. Для ее исправления надо создать в корне проекта файл `.env` и скопироват содержимое `.env.prod` в созданный ранее файл и перезапустить команду сборки контейнеров
* При запуске сборки контейнеров в `docker-compose.yml` может бытб ошибка миграций, связанная с отсуствием какой-либо базы данных. Либо следует вручную создать ее, либо удалить из корня дирректорию `postgres_data`, остановвить контейнер с postgres, удалить его и выполнить команду `docker compose -f .\docker-compose-main-services.yml up postgres_service --build`, после чего выполнить `docker compose up --build`

## Описание выполненных работ на летней практике

### Задачи
* [ ] Подключить CI\CD к проекту
* [ ] Настроить автоматическую сборку проекта
* [ ] Улучшить какой-либо функционал в проекте


### Ход работы
Для **CI\CD** выбран Jenkins, так как я не хотел зависеть от выбранной платформы GIT, например, gitlab, поэтому решил изучить универсальный инструмент

**В данном проекте подразумевается:**

* Сборка проекта (CI) - создание нового docker образа
* Деплой проекта (CD) - запуск необходимых контейнеров на хост машине, то есть локально
, из созданных образов

**Подключение Jenkins**

Для подключения Jenkins выполнил следующие шаги:

* Создание **Jenkinsfile**, в моем случае - это **deploy.jenkins**, который находится в корне проекта 
* Написание необходимого скрипта для сборки и деплоя, в файле описаны этапы, названия для которых разработчик придумывает сам, этапов может сколько угодно
  * Данный файл - скрипт сборки, он необязателен, так как в WEB-интерфейсе можно сделать то же самое
* Я решил запустить Jenkins в docker container 
  * Образ Jenkins содержит дополнения к базовому образу, все описано в файле `./jenkins/Dockerfile`
  * Использовал базовый образ `jenkins/jenkins:lts-jdk11` (jdk11 считается уже устаревшим, при необходимости обновить, можно использовать просто новый базовый образ)
  * Дополнения к базовому образу:
    * установка docker для того, чтобы jenkins мог взаимодействовать с docker на хост машине, далее я пробросил `docker.sock` с хост машины в контейнер к jenkins
    * установка плагинов, которых нет среди базовых, которые предлагает jenkins при первом запуске
* Запуск Jenkins 
  * Для запуска я выбрал вариант с docker-compose, так как это упрощает конфигурацию запуска и легко читается `docker-compose-main-services.yml` (в данном файле я так же указал запуск Postgresql, он не имеет отношения к Jenkins, но так проще запускать в целом весь проект), вся конфигурация указана в этом файле в соответствующем сервисе
  * После запуска контейнеров надо зайти на [http://127.0.0.1:8777](http://127.0.0.1:8777), если это первый запуск, то надо указать код доступа (далее это будет паролем, если его не менять), код печатается в консоль контейнера, если забыли, то он так же продублирован в файлах Jenkins `jenkins_home/secrets/initialAdminPassword`, можно выполнить команду в консоли, чтобы посмотреть содержимое данного файла `docker exec -t jenkins-container sh -c "cat jenkins_home/secrets/initialAdminPassword"`
  * Далее нужно создать Item, назвать его и начать конфигурировать
    * Так как скрипт сборки и деплоя уже есть (deploy.jenkins), то это упростит этап конфигурирования. Надо просто указать в SCM ссылку на GIT репозиторий и указать путь к файл deploy.jenkins (если репозиторий закрыт, то надо будет указать ключи доступа или данные от аккаунта, у которого уже есть доступ к репозиторию)
    * Запускать скрипт можно: вручную, интервально, например, каждые 5 мин, или при появлении изменений в репозитории
    * Для интервального запуска надо найти соответсвующий раздел и указать интервал запуска (примеры, как указывать есть в подсказках в соответсвующем пункте)
    * Для запуска только при наличии изменений в репозитории надо в вашем GIT сервисе настроить вебхуки к вашему Jenkins серверу, а в настройках Item (который создали ранее и начали конфигурировать) найти пункт связанные с данным функционалом, так как у меня все работает локально, а проект лежит на GitHub, я не могу настроить вубхуки с GitHub на локальный сервер

**Автоматическая сборка и деплой проекта**

В данном разделе рассмотрим файл `deploy.jenkins`

```
pipeline {
    agent any

    environment {
       FAST_API_SERVICE = "fast-api-service"
       FAST_API_CONTAINER = "fast-api-container"
       FAST_API_IMAGE = "fast-api:latest"

       ALEMBIC_SERVICE = "alembic_runner"
       ALEMBIC_CONTAINER = "alembic-container"

       ENV_FILE = ".env.prod"

       DOCKER_NETWORK = "services_network"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/raison-collab/TutorialServiceFastAPI.git'
            }
        }

        stage('Test') {
            steps {
                script {
                    sh """
                    docker ps -q --filter "name=alembic-container-test" | xargs --no-run-if-empty docker rm -f "alembic-container-test"


                    docker run --name alembic-container-test \
                        --env-file .env.prod \
                        --network ${DOCKER_NETWORK} \
                        --rm \
                        -d fast-api sh -c "pytest ./tests"
                    """
                }
            }
        }

        stage('Deploy') {
           steps {
               script {
                   // Остановка и удаление старого контейнера
                   sh """
                   docker stop ${FAST_API_CONTAINER} ${ALEMBIC_CONTAINER}
                   docker rm -f ${FAST_API_CONTAINER} ${ALEMBIC_CONTAINER}

                   docker compose --env-file $ENV_FILE build $FAST_API_SERVICE $ALEMBIC_SERVICE

                   docker run --name alembic-container \
                        --env-file .env.prod \
                        --network ${DOCKER_NETWORK} \
                        -d fast-api:latest /bin/sh ./docker/alembic.sh

                   docker run --name fast-api-container \
                       --env-file .env.prod \
                       -p 8887:8887 \
                       --network ${DOCKER_NETWORK} \
                       -d fast-api:latest python3.12 -m uvicorn main:app --host 0.0.0.0 --port 8887
                   """
               }
           }
        }
    }

    post {
       always {
           cleanWs()
       }
    }
}
```

* Конфигурирование начинается с `pipline{}` и внутри пишутся инструкции и конфигурацию
  * `agent` здесь указывает агент, который будет заниматься данным pipline, `any` указывает на то, что любой в "случайном" порядке может заняться этим pipline
  * `environment{}` указываются переменные и их значения, которые будут использовать далее
  * `stages{}` внутри указываются те самые стадии сборки и деплоя проекта
    * `stage()` обозначение стадии, в качестве аргумента передается строка с названием стадии
      * `steps{}` внутри указываются шаги для данного этапа 
        * Иногда встречается ключевое слово `script{}` внутри него указывает какой-либо скрипт, в данном случае я использовал только bash скрипты
  * `post{}` это указывает на то, что будет выполняться после всех этапов
    * `always{}` указывает, на то, что все, что внутри него должно выполняться всегда, независимо от того, что было до него, выполнились ли успешно прошлые стадии или нет
      * `cleanWs()` очищает рабочее место jenkins, удаляет "мусор", является хорошей практикой, в перспективе помогает избежать многих проблем


### Добавленный функционал

Было решено добавить тесты, так как я хотел сделать стадию тестирования, и на мой взгляд это было наилучшим улучшением функционала проекта для сочетания с заданием для летней практики

Для написания тестов я использовал pytest и его версию для асинхронных функций (именно такой подход использовался в проекте) pytest-asyncio и httpx для тестирования endpoint'ов

Все тесты находятся в директории `tests`

Для тестов используется отдельная тестовая база данных, она создается в момент создания контейнера для Postgresql, скрипт создания базы данных находится `./docker/init_db.sh`, а так же свой отдельный клиент, он указан в `./tests/conftest.py`


### Как это работает

Рассмотрим вариант, когда Item настроен так, что он каждые 5 мин опрашивает GIT сервис

* Jenkins делает запрос на GIT сервис в указанный репозиторий, берет последний коммит оттуда (можно настроить так, чтобы это случалось только если есть новые коммиты), это на стадии "Checkout"
* Стадия "Test". Jenkins прогоняет написанный тесты, удаляет указанные контейнеры, чтобы не ломать логику и создавать много новых, это сделано в целях экономии ресурсов, он собирает образ проекта из кода, который получил на прошлой стадии, и начинает тестирование, если тесты пройдены успешно, то он идет к следующему этапу
* Стадия "Deploy". Jenkins останавливает запущенные контейнеры старой версии проекта, удаляет их и создает новые с такими же названиями, но уже с новым образом. Так как образ уже был создан на прошлой стадии, то он и будет использоваться для создания контейнеров
* Через 5 минут все повторяется 

## Выполненные задачи
* [X] Подключено CI\CD. Выбрал Jenkins
* [X] Настроена автоматическая сборка проекта 
* [X] Улучшен функционал. Добавлены тесты, а так же интегрированы в сборку проекта 
