from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    """Кастомная модель Пользователя"""
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=32,
        unique=True
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    """Подписки пользователей"""
    author = models.ForeignKey(
        MyUser,
        verbose_name='Автор рецепта',
        related_name='subscribers',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        MyUser,
        verbose_name='Подписчики',
        related_name='subscriptions',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user.username} -> {self.author.username}'