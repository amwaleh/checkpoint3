from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import index, listBucketlists, login

urlpatterns = patterns('',

    url(r'^/', index),
    url(r'^bucketlists/$',listBucketlists),
    url(r'^login/$',login),
)