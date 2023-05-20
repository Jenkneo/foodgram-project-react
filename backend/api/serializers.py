from drf_base64.fields import Base64ImageField
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, AmountIngredient
from users.models import Favorites, Carts

User = get_user_model()

# ----------------------- Ингредиенты -----------------------


class RecipeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = ('image', 'name')


# ----------------------- Пользователи -----------------------


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed'
        )

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        if self.context.get('request'):
            return user.subscriptions.filter(author=author).exists()


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        if self.context.get('request'):
            return user.subscriptions.filter(author=author).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        limit = self.context.get('request').GET.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeMiniSerializer(recipes, many=True)
        return serializer.data


class UserSubscribeAuthorSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeMiniSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'recipes',
            'recipes_count')
        read_only_fields = '__all__',

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        if self.context.get('request'):
            return user.subscriptions.filter(author=author).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

# ----------------------- Теги -----------------------


class TagSerializer(serializers.ModelSerializer):
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
    """
        Model:  AmountIngredient
        Desc.:  Вспомогательный сериализатор
                Используется для связи между рецептами и ингредиентами
    """
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
        Desc.:  Вспомогательный сериализатор для создания и получения
                ингридиентов для модели RecipeCreateSerializer
    """
    id = serializers.IntegerField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


# ----------------------- Ингредиенты -----------------------


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
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

    def get_ingredients(self, obj):
        queryset = AmountIngredient.objects.filter(recipe=obj)
        return IngredientRecipeReadSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Favorites.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, instance):
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        return Carts.objects.filter(
            user=user,
            recipe=instance
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
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
        fields = '__all__'

    def validate(self, instance):
        if not instance.get('tags') or not instance.get('ingredients'):
            raise serializers.ValidationError(
                'Вы не добавили ни одного тега или ингридента'
            )

        ingr_list = [
            ingredient.get('id') for ingredient in instance.get('ingredients')
        ]
        dub = {
            ingr for ingr in ingr_list if ingr_list.count(ingr) > 1
        }
        err_msg = 'Проверьте правильность заполнения ингредиентов. '
        err_msg += 'Они не должны повторяться.'

        if len(dub) != 0:
            raise serializers.ValidationError(err_msg)
        return instance

    def set_ingredients(self, recipe, ingredients):
        """
            Вспомогательная функция для установки тегов и ингридиентов в рецепт
        """
        ingr_list = []
        for ingredient in ingredients:
            ingr_list.append(
                AmountIngredient(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(pk=ingredient['id']),
                    amount=ingredient['amount']
                )
            )
        AmountIngredient.objects.bulk_create(ingr_list)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data)
        recipe.tags.set(tags)
        self.set_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.text = validated_data.get('text', instance.text)
        ingredients = validated_data.pop('ingredients')
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)

        AmountIngredient.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()
        ).delete()
        instance.tags.set(tags)
        self.set_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data
