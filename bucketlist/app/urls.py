from django.conf.urls import patterns, include, url
import views
urlpatterns = patterns('',
url(r'^users/', views.UserList.as_view()),
url(r'^bucketlists/(?P<id>\d+)/items/(?P<item_id>\d+)/$', views.EditBucketitemsView.as_view()),
url(r'^bucketlists/(?P<id>[0-9]+)/items/$', views.BucketitemsView.as_view()),
url(r'^bucketlists/(?P<id>[0-9]+)/$', views.EditBucketlists.as_view()),
url(r'^bucketlists/$', views.Bucketlists.as_view()),
url(r'^api-token', 'rest_framework.authtoken.views.obtain_auth_token'),
url(r'^docs/', include('rest_framework_swagger.urls')),
)