# Payment System REST API

Асинхронное веб-приложение для управления пользователями, счетами и платежами. Является тестовым заданием для DimaTech.org

## Технологический стек

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM
- **Docker & Docker Compose** - контейнеризация

## Возможности

### Пользователи
- Авторизация по email/password
- Просмотр своих данных
- Просмотр списка счетов и балансов
- Просмотр истории платежей

### Администраторы
- Авторизация по email/password
- Управление пользователями (CRUD)
- Просмотр всех пользователей и их счетов

### Платежная система
- Обработка вебхуков от платежных систем
- Проверка подписи транзакций
- Автоматическое создание счетов
- Защита от дублирования транзакций

## Установка и запуск

### С использованием Docker Compose (рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone git@github.com:kakashi-hatake3/payment-system.git
cd payment-system
```
2. Настройте переменные окружения в `.env`

3. Запустите приложение:
```bash
docker-compose up --build
```
Приложение будет доступно по адресу: http://localhost:8000

### Без Docker

1. Установите PostgreSQL и создайте базу данных:

```bash
createdb payment_db
```

2. Создайте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:

5. Запустите приложение:

```bash
uvicorn app.main:app --reload
```

## API документация
[Swagger UI](http://localhost:8000/docs)
##### Для авторизации нажмите `Authorize` в Swagger UI или вызовите ручку `/auth/token`.
##### Учетка для тестирования пользователя: `email`: `user@example.com`, `password`: `userpassword123`
##### Учетка для тестирования администратора: `email`: `admin@example.com`, `password`: `adminpassword123`
