
# Проект YaMDb
Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории, им  может быть присвоен жанр из списка предустановленных. 
Пользователи могут оставлить к произведениям текстовые отзывы и ставить произведению оценку, оставлять комментарии к отзывам.

### Содержание:
 - [Реализованы возможности](#реализованы-возможности)
 - [Примеры запросов](#примеры-запросов)
 - [Как запустить проект](#как-запустить-проект)
 - [Авторы](#авторы)


### Реализованы возможности
* Получение, создание, удаление категорий произведения.
* Получение, создание, удаление жанров произведения.
* Получение, создание, обновление, удаление произведений.
* Получение, создание, обновление, удаление отзывов.
* Получение, создание, обновление, удаление комментариев к отзыву.
* Получение, создание, обновление, удаление пользователей.
* Регистрация пользователей и выдача токенов


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Esperansa08/api_yamdb.git
```
```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```
```
Для Windows:
env/Scripts/activate

Для Linux или macos
source env/bin/activate
```
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```


### Примеры запросов

#### Публикация и получение категорий

Request: [GET] http://127.0.0.1:8000/api/v1/categories/

Response:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
Request: [POST] http://127.0.0.1:8000/api/v1/categories/

Response:
```
{
  "name": "string",
  "slug": "string"
}
```

#### Частичное обновление и получение произведений
Request: [GET] http://127.0.0.1:8000/api/v1/titles/

Response:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
Request: [PATCH] http://127.0.0.1:8000/api/v1/titles/{titles_id}/

Response:
```
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

#### Публикация и удаление комментария

Request: [POST] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Response:
```
{
  "text": "string"
}
```
Request: [DELETE] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/



### Авторы:
 * Савельева Анастасия (Visteria09@yandex.ru, https://github.com/Esperansa08)
 * Решетников Андрей (reshetnikov.andr@yandex.ru, https://github.com/AndreyUN)
 * Реутов Александр (Sreutov2008@yandex.ru, https://github.com/Sreutov2008)

