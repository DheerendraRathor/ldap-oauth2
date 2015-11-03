from django.conf.urls import url

from .views import ApplicationRegistrationView, ApplicationUpdateView, CustomAuthorizationView

urlpatterns = [
    url(r'^authorize/$', CustomAuthorizationView.as_view(), name='authorize'),
    url(r'^applications/register/$', ApplicationRegistrationView.as_view(), name='register'),
    url(r'^applications/(?P<pk>\d+)/update/$', ApplicationUpdateView.as_view(), name='update'),
]
