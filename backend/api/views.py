from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import PageLimitPaginator
from .serializers import (
    UserListSerializer,
    UserCreateSerializer,
    UserPasswordSerializer)


User = get_user_model()


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageLimitPaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserListSerializer
        return UserCreateSerializer

    @action(detail=False, methods=['get'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserListSerializer(request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = UserPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'detail': 'Пароль успешно изменен!'},
                        status=status.HTTP_204_NO_CONTENT)
