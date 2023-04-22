from django.contrib import admin

from .models import Ingredient, Tag, Recipe, AmountIngredient

admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(AmountIngredient)
