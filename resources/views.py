from oauth2_provider.ext.rest_framework.permissions import TokenHasScope
from rest_framework import viewsets
from rest_framework.decorators import list_route

from core.pagination import DefaultLimitOffsetPagination
from user_resource.models import InstituteAddress

from .serializers import UserRoomSerializer


class ResourcesViewset(viewsets.GenericViewSet):

    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [TokenHasScope]
    required_scopes = ['priv_rooms']

    @list_route(methods=['GET'], serializer_class=UserRoomSerializer)
    def rooms(self, request):
        queryset = InstituteAddress.objects.all().order_by('id').prefetch_related('user__userprofile')
        queryset = self.paginate_queryset(queryset)
        serialized_queryset = self.serializer_class(queryset, many=True)
        return self.get_paginated_response(serialized_queryset.data)
