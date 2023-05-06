from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]

# Мануальное тестирование

# Регистрация пользователя / [POST] api/users
#   Создание пользователя - OK

# Список пользователей / [GET] api/users -
#   Вывод списка - OK
#   Вывод конкретного пользователя - OK
#   Параметр limit - OK
#   Параметр page - OK
#
# Получение токена авторизации / [POST] api/auth/token/login/
#   Получение токена - OK
#   Изменение пароля - OK
#   Использование токена - OK
#   Удаление токена - ОК