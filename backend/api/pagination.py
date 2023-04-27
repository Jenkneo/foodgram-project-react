from rest_framework.pagination import PageNumberPagination


class CustomPaginatior(PageNumberPagination):
    """Пагинатор с определением атрибута page_size_query_param
    Выводит запрошенное количества объектов
    """
    page_size_query_param = 'limit'