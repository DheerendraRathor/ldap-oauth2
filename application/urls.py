__author__ = 'dheerendra'

from django.conf.urls import include, url
import oauth2_provider.urls
from views import ApplicationRegistrationView, ApplicationUpdateView, CustomAuthorizationView

urlpatterns = [
    url(r'^authorize/$', CustomAuthorizationView.as_view(), name='authorize'),
    url(r'^applications/register/$', ApplicationRegistrationView.as_view(), name='register'),
    url(r'^applications/(?P<pk>\d+)/update/$', ApplicationUpdateView.as_view(), name='update'),
]
