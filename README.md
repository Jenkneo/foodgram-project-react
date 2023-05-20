
# Проект 16 спринта: Диплом

## Описание проекта

Foodgram - онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», и перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Подготовка проекта

1. Клонируйте репозиторий:
```      
тут должно быть много текста и инструкций, но я пока не закончил проект
```
## Донастройка проекта
1. Подключитесь по ssh и соберите статистические файлы:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
2. Примените миграции.
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```
3. Создайте суперпользователя.
```
sudo docker-compose exec web python manage.py createsuperuser
```
4. Подключитесь к postgres и импоритруйте данные из CSV.


## Технологии
### Python
- Python X.X-slim
- Django X.X
- Django Rest Framework X.X.X
- Gunicorn X.X.X

### Сервер
- Nginx X.X.X

### База данных
- PostgreSQL X.X

### Контейнер
- Docker X.X.X
- Docker Compose X.X.X

## О проекте
Идея проекта - [Яндекс Практикум](https://practicum.yandex.ru/) 
