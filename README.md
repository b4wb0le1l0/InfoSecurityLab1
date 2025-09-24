# Безопасное REST API с интеграцией CI/CD

Реализация безопасного REST API на Python с интегрированным CI/CD пайплайном для сканирования безопасности.

## Возможности

- Аутентификация пользователей с помощью JWT токенов
- CRUD операции для задач
- Защита от SQL-инъекций (SQLi)
- Защита от межсайтового скриптинга (XSS)
- Безопасное хранение паролей с хешированием
- CI/CD пайплайн с автоматизированным сканированием безопасности

## Реализованные меры безопасности

### 1. Защита от SQL-инъекций (SQLi)
- Использование SQLAlchemy ORM для всех операций с базой данных
- Отсутствие сырых SQL запросов или конкатенации строк для построения запросов
- Параметризованные запросы через методы ORM

### 2. Защита от межсайтового скриптинга (XSS)
- Все пользовательские вводы санируются с помощью библиотеки Bleach
- Кодирование вывода при возврате данных в API ответах
- Заголовки политики безопасности контента

### 3. Безопасная аутентификация
- JWT токены для бессостоятельной аутентификации
- Хеширование паролей с использованием утилит безопасности Werkzeug
- Механизмы истечения срока действия и обновления токенов
- Безопасное хранение секретов и ключей

### 4. Валидация ввода
- Валидация данных с использованием схем Marshmallow
- Проверка типов и ограничений длины
- Валидация обязательных полей

## API Endpoint'ы

### Аутентификация
- `POST /auth/sign-in` - Аутентификация пользователя и получение JWT токена
- `POST /auth/sign-up` - Регистрация нового пользователя

### Управление данными
- `GET /api/data/` - Получение всех задач (требуется аутентификация)
- `GET /api/data/<id>` - Получение конкретной задачи (требуется аутентификация)
- `POST /api/data/` - Создание новой задачи (требуется аутентификация)
- `PUT /api/data/<id>` - Обновление существующей задачи (требуется аутентификация)
- `DELETE /api/data/<id>` - Удаление задачи (требуется аутентификация)

## Установка и настройка

1. Создание виртуального окружения:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Установка зависимостей:
   ```bash
   pip install -r requirements.txt
   ```

3. Установка OWASP Dependency-Check:
  ```bash
  wget https://github.com/jeremylong/DependencyCheck/releases/download/v8.3.1/dependency-check-8.3.1-release.zip
  sunzip dependency-check-8.3.1-release.zip -d dependency-check
  ```

3. Развертывание docker контейнера с Postgres:
   ```bash
   docker-compose up -d
   ```

4. Запуск:
   ```bash
   python main.py
   ```

API доступен по адресу `http://localhost:5000`.

## CI/CD Пайплайн

1. **SAST (Статический анализ безопасности приложений)**:
   - Bandit сканирует код на наличие распространенных проблем безопасности
   - Генерирует JSON отчеты о находках

2. **SCA (Анализ состава программного обеспечения)**:
   - Safety проверяет зависимости на наличие известных уязвимостей
   - Генерирует JSON отчеты о находках

Отчеты загружаются как артефакты и могут быть скачаны для просмотра.

## Тестирование API

Можно епротестировать API с помощью curl или инструмента типа Postman:

1. Регистрация нового пользователя

```bash
curl -X POST http://localhost:5000/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }'
```

2. Аутентификация пользователя

```bash
curl -X POST http://localhost:5000/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }'
```

После успешной аутентификации мы получаем токен доступа, который используем в последующих запросах.

3. Создание новой задачи

```bash
curl -X POST http://localhost:5000/api/data/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Тестовая задача",
    "description": "Описание тестовой задачи"
  }'
```

4. Get всех задач

```bash
curl -X GET http://localhost:5000/api/data/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

5. Get задачи по ID

```bash
curl -X GET http://localhost:5000/api/data/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

6. Update существующей задачи

```bash
curl -X PUT http://localhost:5000/api/data/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Обновленная задача",
    "description": "Обновленное описание задачи"
  }'
```

7. Удаление задачки

```bash
curl -X DELETE http://localhost:5000/api/data/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```


## Отчеты о безопасности

После выполнения CI/CD пайплайна вы можете скачать отчеты о безопасности из артефактов GitHub Actions:
- `bandit-security-report`: Результаты SAST сканирования Bandit
- `safety-dependency-report`: Результаты SCA сканирования Safety

Эти отчеты покажут все проблемы безопасности, найденные в процессе сканирования.
