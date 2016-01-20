from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import index, listBucketlists, login, listItems, editItems

urlpatterns = patterns('',

    url(r'^$', index),
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<item>\d+)/$',editItems),
    url(r'^bucketlists/(?P<id>[0-9]+)/items/$',listItems),
    url(r'^bucketlists/(?P<id>[0-9]+)/',listItems),
    url(r'^bucketlists/$',listBucketlists),
    url(r'^login/',login),
)