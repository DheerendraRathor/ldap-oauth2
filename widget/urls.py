from django.conf.urls import url

from .views import LoginWidget

urlpatterns = [
    url(r'login/$', LoginWidget.as_view(), name='login'),
]
