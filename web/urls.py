from django.conf.urls import patterns, url
from views import (index, list_bucketlists, login,
                   list_items, edit_items, signup, logout)

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^bucketlists/(?P<id>\d+)/items/(?P<item>\d+)/$',
                           edit_items),
                       url(r'^bucketlists/(?P<id>[0-9]+)/items/$', list_items),
                       url(r'^bucketlists/(?P<id>[0-9]+)/', list_items),
                       url(r'^bucketlists/$', list_bucketlists),
                       url(r'^login/', login),
                       url(r'^signup/', signup),
                       url(r'^logout/', logout),

                       )
