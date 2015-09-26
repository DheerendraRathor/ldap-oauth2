from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import UserViewset, UserApplicationListView, ApplicationRevokeView, UserHomePageView


router = DefaultRouter()
router.register('user', UserViewset, base_name='user')


urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^$', UserHomePageView.as_view(), name='home'),
    url(r'^settings/', UserApplicationListView.as_view(), name='settings'),
    url(r'^revoke_app/(?P<pk>\d+)/', ApplicationRevokeView.as_view(), name='revoke_app'),
]