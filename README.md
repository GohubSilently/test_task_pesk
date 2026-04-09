# Тестовое задание для 'ПЭСК'

[![Python](https://img.shields.io/badge/-Python_3.13-3771a1?style=flat&logo=Python&logoColor=ffffff)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat&logo=FastAPI&logoColor=ffffff)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Database-Redis-red?logo=redis)](https://redis.io)

Автор - [Халин Вадим](https://t.me/gohub1)

---

## Оглавление:
- [Описание](#описание)
- [Структура проекта](#структура-проекта)
- [Технологии](#технологии)
- [Локальный запуск](#локальный-запуск)

---

## Описание:
Реализована система **аутентификации и авторизации** на основе JWT с использованием Redis для управления жизненным циклом токенов.

Основные возможности:
- JWT access / refresh токены
- blacklist access токенов
- whitelist refresh токенов
- logout с инвалидированием токенов
- rotation refresh токенов
- ролевая модель доступа (RBAC)
- контейнеризация приложения

Redis используется как централизованное хранилище состояния токенов, что позволяет отзывать JWT до истечения срока действия.

### Авторизация

#### Login
Пользователь получает:
- `access_token` — короткоживущий
- `refresh_token` — долгоживущий

Refresh токен сохраняется в Redis (whitelist).

#### Проверка доступа
При каждом запросе:
1. Проверяется подпись JWT
2. Проверяется отсутствие токена в blacklist Redis
3. Проверяется роль пользователя


#### Refresh
При обновлении:
- старый refresh токен удаляется
- создаётся новая пара токенов
- новый refresh добавляется в whitelist

Это предотвращает повторное использование украденных токенов.

#### Logout

- access token → добавляется в blacklist (TTL = время жизни)
- refresh token → удаляется из whitelist

### Система ролей
Реализован RBAC.

Роли:
- `user`
- `moderator`
- `admin`

Доступ к контенту:

| Endpoint             | user  | moderator  | admin |
|----------------------|-------|------------|-------|
| `/content/user`      | ✅     | ✅          | ✅     |
| `/content/moderator` | ❌     | ✅          | ✅     |
| `/content/admin`     |   ❌    |      ❌      | ✅     |

### Redis структура
- `whitelist:<jti> -> user_id`
- `blacklist:<jti> -> Отклонен`

TTL записей соответствует времени жизни токенов.

### Безопасность
Возможные утечки:
- XSS
- утечка токенов из логов
- повторное использование refresh token
- MITM без HTTPS

Механизмы защиты:
- короткий TTL access token
- refresh rotation
- blacklist/whitelist Redis
- уникальный `jti` для каждого токена
- отзыв токенов через Redis

---

## Структура проекта:
```text
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── content.py
│   │   ├── __init__.py
│   │   └── routers.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── roles.py
│   │   └── utils.py
│   ├── __init__.py
│   └── main.py
├── .env.example
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Технологии:
- Python
- FastAPI
- Redis

---

## Локальный запуск:
1. Клонируем репозиторий.
```
git clone git@github.com:GohubSilently/test_task_pesk.git
cd test_task_pesk
```

2. Создаем .env.
```
APP_TITLE=Тестовое задаени для 'ПЭСК'
APP_DESCRIPTION=Система аутентификации и авторизации - Redis

JWT_SECRET_KEY=secrets.token_hex(32)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXP=900
JWT_REFRESH_TOKEN_EXP=3600


REDIS_HOST=localhost
REDIS_PORT=6379

```

3. Запускаем проект.
```
uv run uvicorn app.main:app --reload
```

Переходим на endpoint - [Ссылка](http://127.0.0.1:8000/docs)


---

## Запуск с помощью Docker.
```
docker compose up --build
```

Переходим на endpoint - [Ссылка](http://localhost:8000/docs)

---
