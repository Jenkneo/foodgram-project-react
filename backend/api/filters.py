from rest_framework.filters import SearchFilter
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_in_shopping_cart', 'is_favorited')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous or not value:
            return queryset
        return queryset.filter(in_favorites__user=user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous or not value:
            return queryset
        return queryset.filter(in_carts__user=user)
