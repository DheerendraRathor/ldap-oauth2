from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views.api import UserViewset
from .views.home import (ApplicationRevokeView, UpdateInstiAddressView, UpdateMobileNumberView, UpdateProgramView,
                         UpdateSecondaryEmailView, UpdateUserProfilePicture, UpdateUserSex, UserApplicationListView,
                         UserHomePageView)

router = DefaultRouter()
router.register('user', UserViewset, base_name='user')

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^$', UserHomePageView.as_view(), name='home'),
    url(r'^update_pp/$', UpdateUserProfilePicture.as_view(), name='update_pp'),
    url(r'^update_address/$', UpdateInstiAddressView.as_view(), name='update_address'),
    url(r'^update_program/$', UpdateProgramView.as_view(), name='update_program'),
    url(r'^update_mobile/$', UpdateMobileNumberView.as_view(), name='update_mobile'),
    url(r'^update_email/$', UpdateSecondaryEmailView.as_view(), name='update_email'),
    url(r'^update_sex/$', UpdateUserSex.as_view(), name='update_sex'),
    url(r'^settings/$', UserApplicationListView.as_view(), name='settings'),
    url(r'^revoke_app/(?P<pk>\d+)/$', ApplicationRevokeView.as_view(), name='revoke_app'),
]
