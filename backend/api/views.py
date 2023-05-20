from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import PageLimitPaginator
from .permissions import IsAuthorOrReadOnly
from .filters import IngredientFilter, RecipeFilter
from . import serializers
from users.models import Subscriptions, Favorites, Carts
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    AmountIngredient
)

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageLimitPaginator

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
        pagination_class=PageLimitPaginator
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        page = self.paginate_queryset(queryset)
        serializer = serializers.UserSubscriptionsSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])
        user = request.user

        if user == author:
            return Response(
                {'message': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        check_sub = Subscriptions.objects.filter(
            author_id=author.id,
            user_id=user.id
        ).exists()

        if request.method == 'POST':
            if check_sub:
                return Response(
                    {'message': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                serializer = serializers.UserSubscribeAuthorSerializer(
                    author,
                    data=request.data,
                    context={"request": request}
                )
                serializer.is_valid(raise_exception=True)
                Subscriptions.objects.create(
                    user=user,
                    author=author
                )

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

        if request.method == 'DELETE':
            if not check_sub:

                return Response(
                    {'message': 'Вы уже отписаны'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                get_object_or_404(
                    Subscriptions,
                    user=user,
                    author=author
                ).delete()

                return Response(
                    {'message': 'Успешная отписка'},
                    status=status.HTTP_204_NO_CONTENT
                )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageLimitPaginator
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeSerializer
        return serializers.RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = serializers.RecipeMiniSerializer(
                recipe,
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            favorite_recipe = Favorites.objects.filter(
                user=user,
                recipe=recipe
            )

            if favorite_recipe.exists():
                return Response(
                    {'message': 'Рецепт уже добавлен в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                Favorites.objects.create(user=user, recipe=recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

        elif request.method == 'DELETE':
            recipe = get_object_or_404(Favorites, user=user, recipe=recipe)
            recipe.delete()

            return Response(
                {'message': 'Рецепт удален из избранного.'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = AmountIngredient.objects.filter(
            recipe__in_carts__user=request.user
        ).annotate(
            total_amount=Sum('amount')
        ).values_list(
            'ingredient__name',
            'total_amount',
            'ingredient__measurement_unit'
        )

        file_list = []
        for ingredient in ingredients:
            file_list.append('{} - {} {}.'.format(*ingredient))
        file = HttpResponse('\n'.join(file_list), content_type='text/plain')

        # Название файла автоматически прописывается в фронте?
        return file

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
        pagination_class=None
    )
    def shopping_cart(self, request, pk=None, **kwargs):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = serializers.RecipeMiniSerializer(
                recipe,
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            recipe_in_cart = Carts.objects.filter(
                user=request.user,
                recipe=recipe
            )
            if recipe_in_cart.exists():
                return Response(
                    {'message': 'Рецепт уже добавлен в список.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                Carts.objects.create(user=request.user, recipe=recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

        if request.method == 'DELETE':
            recipe_in_cart = get_object_or_404(
                Carts,
                user=request.user,
                recipe=recipe
            )

            recipe_in_cart.delete()
            return Response(
                {'message': 'Рецепт удален из списка.'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
