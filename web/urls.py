from django.conf.urls import url
from views import (Signup, Login,
                   UpdateItem, DeleteItem, CreateListItems, Logout, Welcome,
                   ListCreateBucketlists, UpdateList, DeleteList, SearchView, GetList)

urlpatterns = [
    url(r'^$', Welcome.as_view()),
    # Items url
    url(r'^bucketlists/(?P<id>[0-9]+)/$',
        GetList.as_view(), name="getlist"),
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<item>\d+)/update',
        UpdateItem.as_view(), name="update-item"),
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<item>\d+)/delete',
        DeleteItem.as_view(), name="delete-item"),
    url(r'^bucketlists/(?P<id>[0-9]+)/items/$',
        CreateListItems.as_view(), name="items"),
    # bucketlist urls
    url(r'^bucketlists/(?P<id>[0-9]+)/update',
        UpdateList.as_view(), name="update-list"),
    url(r'^bucketlists/(?P<id>[0-9]+)/delete',
        DeleteList.as_view(), name="delete-list"),
    url(r'^bucketlists/$', ListCreateBucketlists.as_view(), name="detail"),
    url(r'^search/', SearchView.as_view(), name="search"),
    # User urls
    url(r'^login/', Login.as_view(), name="login"),
    url(r'^signup/', Signup.as_view(), name="signup"),
    url(r'^logout/', Logout.as_view(), name="logout"),
    


]
