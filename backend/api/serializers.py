from django.core import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer
)
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    """
        Model: User
        Method: [GET]
        Desc.: выводит список пользователей
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
                {'username': 'Вы не можете использовать этот username.'}
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
                {'current_password': 'Неправильный пароль.'}
            )
        if (validated_data['current_password']
           == validated_data['new_password']):
            raise serializers.ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data