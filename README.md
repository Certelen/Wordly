# Wordly API
## Описание
API позволяет пользователям заходить под своими никами, создавать лобби, после чего играть в Wordly с другим игроком.

## Технологии
- Python 3.11
- Django 5.0.2
- Django REST Framework 3.14.0

# Установка
## Копирование репозитория
Клонируем репозиторий и переходим в папку проекта:
```
~ git clone git@github.com:Certelen/Wordly.git
~ cd wordly
```

## Развертывание на текущем устройстве:
Устанавливаем и активируем виртуальное окружение из папки с проектом
```
~ py -3.11 -m venv venv
~ . venv/Scripts/activate
```
Устанавливаем требуемые зависимости:
```
~ pip install -r requirements.txt
```

Переходим в папку
```
~ cd wordly
```
Перед первым запуском создаем и выполняем миграции:
```
python manage.py makemigrations players lobbys
python manage.py migrate
```
Создаем суперпользователя, если необходимо:
```
python manage.py createsuperuser
```
# Запуск
Запуск сервиса производится командой:
```
~ py manage.py runserver
```
# Адресные пути
- [Создание пользователя/вход](http://127.0.0.1:8000/login)
- [Админка](http://127.0.0.1:8000/admin)
