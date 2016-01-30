from django.conf.urls import url
from views import (Signup, list_bucketlists, Login,
                   list_items, edit_items, Logout, Welcome)

urlpatterns = [
    url(r'^$', Welcome.as_view()),
    url(r'^bucketlists/(?P<id>\d+)/items/(?P<item>\d+)/$',
        edit_items),
    url(r'^bucketlists/(?P<id>[0-9]+)/items/$', list_items),
    url(r'^bucketlists/(?P<id>[0-9]+)/', list_items),
    url(r'^bucketlists/$', list_bucketlists),
    url(r'^login/', Login.as_view()),
    url(r'^signup/', Signup.as_view()),
    url(r'^logout/', Logout.as_view()),
    url(r'^about/', Signup.as_view()),

]
