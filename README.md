Инструкция по запуску проекта на ОС Linux Ubuntu

Шаг 1. Клонирование репозитория

1. git clone https://github.com/fniad/coursework_6.git
2. cd coursework_6

Шаг 2. Установка зависимостей

1. python3 poetry install
2. poetry shell

Шаг 3. Установка и настройка Redis

1. sudo apt-get install redis-server
2. sudo service redis-server start
3. redis-cli ping (в ответ должно прийти 'PONG')

Шаг 4. Установка и настройка PostgreSQL

1. sudo apt-get install postgresql
2. sudo -u postgres psql
3. CREATE DATABASE seller_message;
4. \q

Шаг 5. Настройка окружения

1. touch .env
2. nano .env и заполнить по шаблону из .env.test

Шаг 6. Применение миграций

1. python3 manage.py migrate

Шаг 7. Загрузка данных с помощью команд 

1. python3 manage.py fill_db

Шаг 8. Создание суперпользователя, а также модератора и блоггера. Раздача прав доступа.

1. python3 manage.py csu
2. python3 manage.py create_groups
3. python3 manage.py create_moderator_and_blogger

Шаг 9. Запуск сервера
1. python3 manage.py runserver
