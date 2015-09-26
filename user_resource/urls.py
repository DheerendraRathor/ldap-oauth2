from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import UserViewset, UserApplicationListView, ApplicationRevokeView, UserHomePageView, UpdateProgramView, \
    UpdateInstiAddressView, UpdateMobileNumberView, UpdateSecondaryEmailView

router = DefaultRouter()
router.register('user', UserViewset, base_name='user')

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^$', UserHomePageView.as_view(), name='home'),
    url(r'^update_address/$', UpdateInstiAddressView.as_view(), name='update_address'),
    url(r'^update_program/$', UpdateProgramView.as_view(), name='update_program'),
    url(r'^update_mobile/$', UpdateMobileNumberView.as_view(), name='update_mobile'),
    url(r'^update_email/$', UpdateSecondaryEmailView.as_view(), name='update_email'),
    url(r'^settings/', UserApplicationListView.as_view(), name='settings'),
    url(r'^revoke_app/(?P<pk>\d+)/', ApplicationRevokeView.as_view(), name='revoke_app'),
]
