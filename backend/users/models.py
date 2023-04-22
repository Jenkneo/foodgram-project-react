from django.db import models
from django.contrib.auth.models import AbstractUser
from recipes.models import Recipe


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


class Favorites(models.Model):
    """Избранные рецепты пользователя"""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Понравившиеся рецепты',
        related_name='in_favorites',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        MyUser,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class Carts(models.Model):
    """Рецепты в корзине покупок"""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в списке покупок',
        related_name='in_carts',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        MyUser,
        verbose_name='Владелец списка',
        related_name='carts',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'
