from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import UserViewset


router = DefaultRouter()
router.register('user', UserViewset, base_name='user')


urlpatterns = [
    url('^api/', include(router.urls, namespace='api')),
]