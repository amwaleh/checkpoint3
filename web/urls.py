from django.conf.urls import url
from views import (Signup, Login,
                   UpdateItem, DeleteItem, CreateListItems, Logout, Welcome,
                   ListCreateBucketlists, UpdateList, DeleteList, SearchView)

urlpatterns = [
    url(r'^$', Welcome.as_view()),
    # Items url
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<item>\d+)/update',
        UpdateItem.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<item>\d+)/delete',
        DeleteItem.as_view()),
    url(r'^bucketlists/(?P<id>[0-9]+)/items/$', CreateListItems.as_view()),
    # bucketlist urls
    url(r'^bucketlists/(?P<id>[0-9]+)/update', UpdateList.as_view()),
    url(r'^bucketlists/(?P<id>[0-9]+)/delete', DeleteList.as_view()),
    url(r'^bucketlists/', ListCreateBucketlists.as_view()),
    url(r'^search/', SearchView.as_view()),
    # User urls
    url(r'^login/', Login.as_view()),
    url(r'^signup/', Signup.as_view()),
    url(r'^logout/', Logout.as_view()),


]
