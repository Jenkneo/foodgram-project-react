# Проект 16 спринта: Диплом  
  
## Описание проекта  
  
Foodgram - онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», и перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.  

Полная документация к API находится по эндпоинту: /api/redoc  
**Данные для админ панели (для ревьюера):**
``` 
Адрес сайта http://158.160.14.36/
email - admin@admin.ru
password - admin
``` 

## Подготовка проекта  
  
1. Клонируйте репозиторий
2. Настройте удаленный сервер
``` 
# Создайте в домашней директории папку nginx
mkdir nginx

#Установите Docker и Docker-compose
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```  
3. Настройте удаленный сервер
``` 
# Скопируйте docker-compose.yaml в домашнюю директорию сервера
scp -rv C:\<путь_до_файла>\docker-compose.yaml <ваш_username>@<ip_сервера>:/home

# Скопируйте nginx.conf в созданную папку nginx
scp -rv C:\<путь_до_файла>\nginx\default.conf <ваш_username>@<ip_сервера>:/home/nginx
``` 
4.  В репозитории на github добавьте secret данные.  `Settings - Secrets and variables - Actions`:
``` 
DB_NAME - Имя базы данных (Например - postgres)
DB_USER - Имя пользователя базы данных (Например - postgres)
DB_PASSWORD - Пароль пользователя базы данных (Например - postgres)

DOCKER_USERNAME - Логин от DockerHub
DOCKER_PASSWORD - Пароль от DockerHub

SSH_HOST - IP адрес вашего удаленного сервера
SSH_KEY - id_rsa закрытого ключа для подключения к серверу
SSH_USER - логин на удаленном сервере
``` 

## Запуск проекта  
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
- Python 3.7-slim  
- Django 3.2  
- Django Rest Framework 3.14.0  
- Gunicorn 20.0.4  
  
### Сервер  
- Nginx 1.19.3  
  
### База данных  
- PostgreSQL 13.0-alpine  
  
### Контейнер  
- Docker 20.10.23 
- Docker Compose 2.15.1  
  
## О проекте  
Идея проекта - [Яндекс Практикум](https://practicum.yandex.ru/)