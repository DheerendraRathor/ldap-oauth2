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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
import account.urls
import application.urls
import oauth2_provider.urls
import user_resource.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include(application.urls, namespace='oauth')),
    url(r'^oauth/', include(oauth2_provider.urls, namespace='oauth2_provider')),
    url(r'^account/', include(account.urls, namespace='account')),
    url(r'^user/', include(user_resource.urls, namespace='user')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
