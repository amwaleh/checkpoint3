from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token

from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework.routers import DefaultRouter
import views
router = DefaultRouter()

router.register(r'users', views.UserViewSet)

router.register(r'bucketlists', views.BucketlistViewset, "bucketlists-detail")
router.register(r'bucketlists/(?P<id>\d+)/items', views.ItemsViewSet, )


urlpatterns = [
    url(r'^api-token/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    #url(r'^docs/', views.schema_view),
    url(r'^', include(router.urls)),

]
