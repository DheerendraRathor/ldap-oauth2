from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import UserViewset, UserApplicationListView, ApplicationRevokeView


router = DefaultRouter()
router.register('user', UserViewset, base_name='user')


urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^$', UserApplicationListView.as_view(), name='index'),
    url(r'^revoke_app/(?P<pk>\d+)/', ApplicationRevokeView.as_view(), name='revoke_app'),
]