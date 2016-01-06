from rest_framework import pagination


class DefaultLimitOffsetPagination(pagination.LimitOffsetPagination):

    default_limit = 20
    max_limit = 500
