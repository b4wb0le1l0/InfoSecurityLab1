# Тестовые запросы для API

## 1. Регистрация нового пользователя

```bash
curl -X POST http://localhost:5000/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }'
```

## 2. Аутентификация пользователя

```bash
curl -X POST http://localhost:5000/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }'
```

После успешной аутентификации мы получаем токен доступа, который используем в последующих запросах.

## 3. Создание новой задачи

```bash
curl -X POST http://localhost:5000/api/data/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Тестовая задача",
    "description": "Описание тестовой задачи"
  }'
```

## 4. Get всех задач

```bash
curl -X GET http://localhost:5000/api/data/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 5. Get задачи по ID

```bash
curl -X GET http://localhost:5000/api/data/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 6. Update существующей задачи

```bash
curl -X PUT http://localhost:5000/api/data/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Обновленная задача",
    "description": "Обновленное описание задачи"
  }'
```

## 7. Удаление задачки

```bash
curl -X DELETE http://localhost:5000/api/data/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
