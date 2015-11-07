"""sso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import re

import jet.dashboard.urls
import jet.urls
import oauth2_provider.urls
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

import account.urls
import application.urls
import user_resource.urls
import widget.urls

from .views import DocView, IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^doc/$', DocView.as_view(), name='doc'),
    url(r'^doc/(?P<tab>[\w-]+\w+)/$', DocView.as_view(), name='doc'),
    url(r'^jet/', include(jet.urls, namespace='jet')),
    url(r'^jet/dashboard/', include(jet.dashboard.urls, namespace='jet-dashboard')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include(application.urls, namespace='oauth')),
    url(r'^oauth/', include(oauth2_provider.urls, namespace='oauth2_provider')),
    url(r'^account/', include(account.urls, namespace='account')),
    url(r'^user/', include(user_resource.urls, namespace='user')),
    url(r'^widget/', include(widget.urls, namespace='widgets'))
]

# Fail safe! If nginx is down, this might come handy.
urlpatterns += [
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), serve,
        kwargs={
            'document_root': settings.STATIC_ROOT,
        }
        ),
    url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve,
        kwargs={
            'document_root': settings.MEDIA_ROOT,
        }
        ),
]
