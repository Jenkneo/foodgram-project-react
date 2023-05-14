from django.core import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer
)
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, AmountIngredient
from users.models import Favorites, Carts, Subscriptions
from django.db.models import F

User = get_user_model()

# ----------------------- Ингредиенты -----------------------


class RecipeMiniSerializer(serializers.ModelSerializer):
    """
        Model:  Recipe
        Method: [GET]
        Desc.:  Выводит список рецептов без ингридиентов.
                Необходима для UserSubscribeAuthorSerializer
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__',


# ----------------------- Пользователи -----------------------


class UserSerializer(serializers.ModelSerializer):
    """
        Model: User
        Method: [GET]
        Desc.: Выводит список пользователей
    """

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name'
        )
        extra_kwargs = {'password': {'write_only': True}}


class UserCreateSerializer(DjoserUserCreateSerializer):
    """
        Model: User
        Method: [POST]
        Desc.: Создает нового пользователя
    """
    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate(self, obj):
        incorrect_usernames = ['me',
                               'admin',
                               'username',
                               'first_name',
                               'last_name']

        if self.initial_data.get('username') in incorrect_usernames:
            raise serializers.ValidationError(
                {'username': 'Введеный username уже используется.'}
            )
        return obj


class UserPasswordSerializer(serializers.Serializer):
    """
        Model: User
        Method: [POST]
        Desc.: Изменяет пароль пользователя
    """
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, obj):
        try:
            validate_password(obj['new_password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )
        return super().validate(obj)

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                {'current_password': 'Неверный пароль.'}
            )
        if (validated_data['current_password']
           == validated_data['new_password']):
            raise serializers.ValidationError(
                {'new_password':
                     'Такой пароль уже используется. Придумайте новый'})
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    """[GET] Список авторов на которых подписан пользователь."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        return Subscriptions.objects.filter(
            user=user,
            author=author
        ).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data


class UserSubscribeAuthorSerializer(serializers.ModelSerializer):
    """[POST, DELETE] Подписка на автора и отписка."""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeMiniSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')
        read_only_fields = '__all__',

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Subscriptions.objects.filter(
            user=self.context['request'].user,
            author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

# ----------------------- Теги -----------------------


class TagSerializer(serializers.ModelSerializer):
    """
        Model: Tag
        Method: [GET]
        Desc.: Получение всего списка тегов
    """
    class Meta:
        model = Tag
        fields = '__all__'


# ----------------------- Ингредиенты -----------------------


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class AmountIngredientCreateSerializer(serializers.ModelSerializer):
    """
        Model:  AmountIngredient
        Method: -
        Desc.:  Вспомогательный сериализатор для создания и получения
                ингридиентов для модели RecipeCreateSerializer
    """
    id = serializers.IntegerField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


# ----------------------- Ингредиенты -----------------------


class RecipeSerializer(serializers.ModelSerializer):
    """
        Model: Recipe
        Method: [GET]
        Desc.: Выводит список рецептов.
    """
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeReadSerializer(
        many=True,
        read_only=True,
        source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'is_favorite',
            'is_shopping_cart',
        )

    def get_is_favorited(self, instance):
        """Проверяем наличие рецепта в избранном"""
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        return Favorites.objects.filter(
            user=user,
            recipe=instance
        ).exists()

    def get_is_in_shopping_cart(self, instance):
        """Проверяем наличие рецепта в списке покупок"""
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        return Carts.objects.filter(
            user=user,
            recipe=instance
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
        Model: Recipe
        Method: [GET, POST, PATCH, DELETE]
        Desc.: Необходим для создания, обновления/изменения и удаления рецепта.
    """
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = UserSerializer(read_only=True)
    id = serializers.ReadOnlyField()
    ingredients = AmountIngredientCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'author',
                  'ingredients',
                  'tags',
                  'image',
                  'name',
                  'text',
                  'cooking_time',
                  )
        read_only_fields = ('author',)
        extra_kwargs = {
            'ingredients': {'required': True, 'allow_blank': False},
            'tags': {'required': True, 'allow_blank': False},
            'name': {'required': True, 'allow_blank': False},
            'text': {'required': True, 'allow_blank': False},
            'image': {'required': True, 'allow_blank': False},
            'cooking_time': {'required': True},
        }

    def validate(self, instance):
        required_fields = ['name', 'text', 'cooking_time']
        for field in required_fields:
            if not instance.get(field):
                raise serializers.ValidationError(
                    f'{field} - Обязательное поле.'
                )

        if not instance.get('tags'):
            raise serializers.ValidationError(
                'Минимально допустимое количетсво тегов - 1'
            )

        if not instance.get('ingredients'):
            raise serializers.ValidationError(
                'Минимально допустимое количетсво ингридиентов - 1'
            )

        inrgedient_id_list = [
            item['id'] for item in instance.get('ingredients')
        ]
        if len(inrgedient_id_list) != len(set(inrgedient_id_list)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )
        return instance

    def tags_ingredients(self, recipe, tags, ingredients):
        """
            Вспомогательная функция для установки тегов и ингридиентов в рецепт
        """
        recipe.tags.set(tags)
        AmountIngredient.objects.bulk_create(
            [
                AmountIngredient(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(pk=ingredient['id']),
                    amount=ingredient['amount']
                ) for ingredient in ingredients
            ]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        self.tags_ingredients(recipe, tags, ingredients)
        return recipe
