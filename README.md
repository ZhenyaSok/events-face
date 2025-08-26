# Events-Face

Сервис для работы с мероприятиями с поддержкой JWT аутентификации и синхронизации с внешним поставщиком `events-provider`.

---

## 📦 Установка зависимостей

Используем `uv` для управления виртуальной средой и зависимостями:

```bash
# Установка uv, если ещё не установлен
pip install uv
```

# Создание виртуальной среды и установка зависимостей
```bash
uv pip install -e .
```
---

### Структура проекта
```
events-face/
├─ src/
│   ├─ config/               # Django проект (settings, asgi, wsgi)
│   │   └─ settings.py
│   │
│   ├─ events/               # Приложение мероприятий
│   ├─ authentication/       # JWT аутентификация
│   ├─ sync/                 # Синхронизация с events-provider
│   ├─ manage.py
│   └─ urls.py               # Эндпоинты
├─ .venv/                    # Виртуальная среда
└─ README.md
```

---

🚀 Запуск сервиса

# Перейти в директорию проекта:
```bash
cd src
```

# Применить миграции:
```bash
uv run python manage.py migrate
```


# Создать суперпользователя (для админки):
```bash
uv run python manage.py createsuperuser
```


# Запустить сервер разработки:
```bash
uv run python manage.py runserver
```

# Сервис будет доступен по адресу: http://127.0.0.1:8000/

🔑 Эндпоинты
### Аутентификация (JWT)

| Метод | URL                     | Описание                                   |
|-------|--------------------------|--------------------------------------------|
| POST  | `/api/auth/register`     | Регистрация нового пользователя            |
| POST  | `/api/auth/login`        | Логин, возвращает Access и Refresh токены  |
| POST  | `/api/auth/token/refresh`| Обновление Access Token по Refresh Token   |
| POST  | `/api/auth/logout`       | Выход, аннулирование Refresh Token         |


### Пример запроса регистрации

```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```
### Мероприятия
| Метод | URL            | Описание                                                                                    |
| ----- | -------------- | ------------------------------------------------------------------------------------------- |
| GET   | `/api/events/` | Список мероприятий (только открытые). Доступ только для авторизованных пользователей (JWT). |


Поддерживается фильтрация по name, сортировка по date и курсорная пагинация.

- Синхронизация с events-provider

Примеры запуска:

Синхронизация за вчерашний день:
```bash
uv run python manage.py sync_events
```

- Синхронизация за конкретную дату:

```bash
uv run python manage.py sync_events --date 2025-03-15
```


- Синхронизация всех мероприятий:
```bash
uv run python manage.py sync_events --all
```


- Результаты каждой синхронизации сохраняются в модели SyncLog.

