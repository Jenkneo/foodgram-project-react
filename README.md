
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
4. Импоритруйте данные из CSV подключившись к postgres.


## Технологии
### Python
- Python 3.7-slim
- Django 3.2
- Django Rest Framework 3.12.4
- Gunicorn 20.0.4

### Сервер
- Nginx 1.21.3

### База данных
- PostgreSQL 13.0

### Контейнер
- Docker 20.10.23
- Docker Compose 2.15.1

## О проекте
Идея проекта - [Яндекс Практикум](https://practicum.yandex.ru/) 

## Эндпоинты
На данный момент доступны и протестированы следующие эндпоиниты:
 
#### Пользователи
 1. [x] [GET] api/users - Список пользователей 
 2. [x] [GET] api/users/{id} - Вывод конкретного пользователя 
 3. [x] [GET] api/users/me - Вывод информации о своем профиле**
	 - [x] parm. LIMIT - вывод определенного кол-ва пользователей
	 - [x] parm. PAGE - вывод определенной страницы пользователей
 4. [x] [POST] api/users - Создание пользователя 
 5. [x] [POST] api/users/set_password - Смена пароля пользователя**
 6. [x] [POST] api/auth/token/login/ - Получение токена авторизации
 7. [x] [POST] api/auth/token/logout/ - Удаление токена авторизации**
  
#### Теги
 1. [x] [GET] api/tag- Список тегов
 2. [x] [GET] api/tag/{id} - Вывод конкретного тега

  #### Рецепты
 1. [x] [GET] api/recipes/- Список рецептов
	 1. [x] parm. page - вывод определенной страницы с рецептами
	 2. [x] parm. limit - вывод определенной количества рецептов на странице
	 3. [ ] parm. is_favorited - вывод рецептов которые нахоядтся у вас в избранном**
	 4. [ ] parm. is_in_shopping_cart - вывод рецептов которые нахоядтся у вас в корзине покупок**
	 5. [x] parm. author - вывод рецептов определенного автора
	 6. [x] parm. tags - вывод рецептов с определенным тегом
 4. [x] [POST] api/recipes/ - Создание рецепта**
 5. [x] [GET]/api/recipes/{id}/ - Вывод определенного рецепта по id
 6. [x] [PATCH]/api/recipes/{id}/ - Удаление определенного рецепта по id**
 7. [x] [DELETE]/api/recipes/{id}/ - Удаление определенного рецепта по id**
  
#### Список покупок
 1. [X] [GET] api/recipes/download_sopping_cart/ - Скачать список покупок**
 2. [X] [POST] api/recipes/{id}/shopping_cart/ - Добавить рецепт в список покупок**
 3. [X] [DELETE] api/recipes/{id}/shopping_cart/ - Удалить рецепт из списка покупок**

#### Избранное
 1. [X] [POST] api/recipes/{id}/favorite/ - Добавить рецепт в избранное**
 2. [X] [DELETE] api/recipes/{id}/favorite/ - Удалить рецепт из избранного**

#### Подписки
 1. [x] [GET] api/users/subsriptions - Вывод подписок пользователя**
    1. [x] parm. page - Номер страницы.
    2. [x] parm. limit - Количество объектов на странице.
    3. [ ] parm. recipe_limit - Количество объектов внутри поля recipes.
 2. [x] [POST] api/users/{id}/subsriptions - Подписка на пользователя**
 3. [x] [DELETE] api/users/{id}/subsriptions - Отписка от пользователя**


#### Ингридиенты
 1. [x] [GET] api/ingredients/- Список ингредиентов
	 1. [x] parm. name - поиск ингредиента по названию
 2. [x] [GET] api/tag/{id} - Вывод конкретного ингредиента


** - доступно только авторизированному пользователю