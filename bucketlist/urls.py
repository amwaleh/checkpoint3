"""bucketlist URL Configuration

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
from django.contrib import admin
from rest_framework.authtoken import views
import app.urls
import web.urls
from rest_framework.routers import DefaultRouter
admin.autodiscover()

# router = DefaultRouter()
# router.register(r'bucketlists',viewsets.BucketlistViewset)

# urlpatterns = router.urls
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # Urls for web
    url(r'^web/', include('web.urls')),
    # urls for api
    url(r'^api/', include('app.urls')),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
]
