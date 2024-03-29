# Api_yamdb


### О чём проект:

Yamdb - сервис, который с помощью API позволяет собирать отзывы 
на произведения искусства, такие как картины, 
музыкальные композиции, фильмы и другие.

У каждого произведения искусства есть название, год создания, категория и жанр.
Всем пользователям доступен просмотр списка всех хранящихся в базе 
произведений, сведений определенного произведения, 
отзывов и комментариев к нему, 
а также просмотр всех хранящихся в базе категорий и жанров.

* Для авторизованных пользователей доступно написание отзывов 
и комментариев к произведениям. 

* Для модераторов доступно написание отзывов и комментариев, 
а также удаление отзывов и комментариев оставленными другими пользователями.

* Для администраторов доступно добавление произведений, 
категорий, жанров; написание отзывов и комментариев; удаление отзывов и 
комментариев, которые оставили другие пользователи.


### Запуск проекта через docker-compose

Клонируйте репозиторий и перейдите в него в командной строке:
``` 
git clone git@github.com:IgorKrupko-94/infra_sp2.git 
```
``` 
cd infra_sp2
```

Настройте приложение для работы с базой данных Postgres, 
для этого оно должно знать все данные для подключения к базе. 
Но секретные ключи, доступы, токены не следует хранить в коде. 
А для работы приложения их нужно передать в контейнер. 
Это можно сделать несколькими способами:
* Прописать переменные окружения прямо в докерфайле, 
для этого есть инструкция ENV:
```
ENV token 12345
```
* Задать переменные окружения при сборке контейнера, 
выполнив команду ```run``` с ключом ```-e```:
```
docker run <IMAGE-NAME> -e token=12345
```
* Создать файл .env и прописать переменные окружения в нём. 
Это самый предпочтительный способ.
Создайте файл .env с переменными окружения для работы с базой данных:
```
nano .env
```
Заполните его:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
В папке infra/ лежит пример файла .env под названием .env.example.
Дальше проект api_yamdb будет работать с PostgreSQL.

Запустите docker-compose командой ```docker-compose up```
Выполните по очереди команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
Теперь проект доступен по адресу http://localhost/.

### Команды для заполнения базы тестовой информацией:

* Создать дамп (резервную копию) базы данных "fixtures.json" можно следующей командой:
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
* Далее команды по востановлению базы данных из резервной копии. Узнаем CONTAINER ID для контейнера с джанго - "infra-web-1":
```
docker container ls -a
```
* Копируем файл "fixtures.json" с фикстурами в контейнер:
```
docker cp fixtures.json <CONTAINER ID>:/app
```
* Применяем фикстуры:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
Удаляем файл "fixtures.json" из контейнера:
```
docker exec -it <CONTAINER ID> bash
rm fixtures.json
exit
```


### Примеры команд для API доступные всем пользователям:

Получение кода подтверждения на почту для нового пользователя

```
POST http://127.0.0.1:8000/api/v1/auth/signup/
    {
    "email": "string",
    "username": "string"
    }
```

Получение токена для зарегестрированного пользователя

```
POST http://127.0.0.1:8000/api/v1/auth/token/
    {
    "username": "string",
    "confirmation_code": "string"
    }
```

Получение списка всех произведений

```
GET http://127.0.0.1:8000/api/v1/titles/
```

Получение списка всех категорий

```
GET http://127.0.0.1:8000/api/v1/categories/
```

Получение списка всех жанров

```
GET http://127.0.0.1:8000/api/v1/genres/
```

Получение списка всех отзывов к произведению

```
GET http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/
```

Добавление отзыва к произведению

```
POST http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/
    {
    "text": "string",
    "score": 10
    }
```

Получение списка всех комментариев к отзыву на произведение

```
GET http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/<reviews_id>/comments/
```

Добавление комментария к отзыву

```
POST http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/<reviews_id>/comments/
    {
    "text": "string"
    }
```

### Примеры команд для API доступные для модераторов 
### (также доступны команды из категории "Все пользователи"):

Изменение отзыва к произведению

```
POST http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/<review_id>
    {
    "text": "string",
    "score": 10
    }
```

Изменение комментария к отзыву

```
POST http://127.0.0.1:8000/api/v1/titles/<title_id>/reviews/comments/<comment_id>
    {
    "text": "string"
    }
```

### Примеры команд для API доступные для администраторов 
### (также доступны команды из категории "Все пользователи" и "модераторы"):

## Произведения

Создание нового произведения в базе

```
POST http://127.0.0.1:8000/api/v1/titles/
    {
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
    }
```

Изменение произведения в базе

```
PATCH http://127.0.0.1:8000/api/v1/titles/<title_id>/
```

Удаление произведения

```
DELETE http://127.0.0.1:8000/api/v1/titles/<title_id>/
```

## Категории

Создание новой категории

```
POST http://127.0.0.1:8000/api/v1/categories/
    {
    "name": "string",
    "slug": "string"
    }
```

Удаление категории

```
DELETE http://127.0.0.1:8000/api/v1/categories/<slug>
```

## Жанры

Создание нового жанра

```
POST http://127.0.0.1:8000/api/v1/genres/
    {
    "name": "string",
    "slug": "string"
    }
```

Удаление жанра

```
DELETE http://127.0.0.1:8000/api/v1/genres/<slug>
```

### Все остальные команды можно посмотреть в документации: 
### http://127.0.0.1:8000/redoc/


# Author
## Igor Krupko