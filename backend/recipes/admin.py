from django.contrib import admin

from .models import Ingredient, Tag, Recipe, AmountIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorite_count')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorite_count',)
    empty_value_display = '-пусто-'

    def favorite_count(self, obj):
        return obj.favorite.count()

    favorite_count.short_description = 'Добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(AmountIngredient)
