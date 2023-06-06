# Продуктовый помощник 

![preview img](frontend/public/favicon.png)
  
## Описание проекта  
  
Foodgram - онлайн-сервис, где пользователи могут публиковать рецепты, 
подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», 
и перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.  

Полная документация к API находится по эндпоинту: /api/redoc  

>❤ Frontend на React создан разработчиками из [Яндекс Практикум](https://practicum.yandex.ru/)


## Технологии
<img src="https://img.shields.io/badge/Python%203.7-grey?style=for-the-badge&logo=Python&logoColor=Blue"> <img src="https://img.shields.io/badge/Django%203.2-grey?style=for-the-badge&logo=Django&logoColor=darkgreen"> <img src="https://img.shields.io/badge/DRF%203.12.0-grey?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/Gunicorn%2020.0.4-grey?style=for-the-badge&logo=Gunicorn&logoColor=green"> <img src="https://img.shields.io/badge/Nginx%201.19.3-grey?style=for-the-badge&logo=Nginx&logoColor=black"> <img src="https://img.shields.io/badge/PostgreSQL%2013.0-grey?style=for-the-badge&logo=PostgreSQL&logoColor=Blue"> <img src="https://img.shields.io/badge/Docker%2020.10.23-grey?style=for-the-badge&logo=Docker&logoColor=Blue"> <img src="https://img.shields.io/badge/Docker Compose%202.15.1-grey?style=for-the-badge&logo=Docker&logoColor=Blue"> <img src="https://img.shields.io/badge/React-ca7370?style=for-the-badge&logo=React&logoColor=lightBlue">


## Подготовка проекта  
  
1. 🔽 Клонируйте репозиторий
```      
git clone https://github.com/Jenkneo/foodgram-project-react
```
2. ⚙️ Настройте удаленный сервер
``` 
# Создайте в домашней директории папку nginx
mkdir nginx

#Установите Docker и Docker-compose
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```  
3. 🔧 Локально соберите frontend контейнер и запушьте его на dockerhub
```
docker push docker/getting-started
```
> Подробнее как собрать и запушить контейнер - [тут](https://docs.docker.com/get-started/04_sharing_app/)


4. ✏️ Отредактируйте docker-compose.yaml (14 и 28 строка):
```
image: <ваш-dockerhub>/foodgram-project-react:latest
```

5. 📤 Отправьте docker-compose.yml и nginx.conf на ваш удаленный сервер
``` 
# Скопируйте docker-compose.yaml в домашнюю директорию сервера
scp -rv C:\<путь_до_файла>\docker-compose.yaml <ваш_username>@<ip_сервера>:/home

# Скопируйте nginx.conf в созданную папку nginx
scp -rv C:\<путь_до_файла>\nginx\default.conf <ваш_username>@<ip_сервера>:/home/nginx
``` 
6. ✏️ В репозитории на github добавьте secret данные.  `Settings - Secrets and variables - Actions`:
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
1. 🔼 Запушьте свой проект на github:
```
git push
```
2. ⌛ Немного подождите когда проект задеплоится на сервер.
3. ⚙️ Подключитесь по ssh и соберите статистические файлы:  
```  
sudo docker-compose exec backend python manage.py collectstatic --no-input  
```  
4. ⚙️ Примените миграции.  
```  
sudo docker-compose exec backend python manage.py makemigrations  
sudo docker-compose exec backend python manage.py migrate  
```  
5. ⚙️ Создайте суперпользователя.  
```  
sudo docker-compose exec web python manage.py createsuperuser  
```  
6. 🔗 Подключитесь к postgres и импоритруйте CSV в postgres из папки /data.  
7. ✅ Проверьте работоспособность проекта перейдя по адресу сервера в браузере.
```
http://<server_ip>/
```
  
## О проекте  
Идея проекта - [Яндекс Практикум](https://practicum.yandex.ru/)