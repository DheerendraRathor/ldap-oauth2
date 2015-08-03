__author__ = 'dheerendra'

from django.conf.urls import include, url
import oauth2_provider.urls
from views import ApplicationRegistrationView, ApplicationDetailView, ApplicationListView, ApplicationUpdateView, \
    ApplicationDeleteView, CustomAuthorizationView

urlpatterns = [
    url(r'^authorize/$', CustomAuthorizationView.as_view(), name='authorize'),
    url(r'^applications/$', ApplicationListView.as_view(), name='list'),
    url(r'^applications/register/$', ApplicationRegistrationView.as_view(), name='register'),
    url(r'^applications/(?P<pk>\d+)/$', ApplicationDetailView.as_view(), name='detail'),
    url(r'^applications/(?P<pk>\d+)/update/$', ApplicationUpdateView.as_view(), name='update'),
    url(r'^applications/(?P<pk>\d+)/delete/$', ApplicationDeleteView.as_view(), name='delete'),
]
