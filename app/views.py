
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from models import Bucketlist, Bucketitems
from serializers import (UserSerializer, BucketlistSerializer,
                         BucketitemSerializer)
from rest_framework import viewsets, mixins


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """This viewset automatically provides `list` and `detail` actions."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST'
                else permissions.IsAuthenticatedOrReadOnly()),


class BucketlistViewset(viewsets.ModelViewSet):
    """Handles Creation and manupulation of Bucketlists."""

    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','id')

    def get_queryset(self):
        # Override method to restrict query to current user

        bucketlist = Bucketlist.objects.filter(creator=self.request.user.id)
        return bucketlist

    def create(self, request):
        # Override to Restrict creator to current user

        request.POST._mutable = True
        request.data['creator'] = request.user.id
        serializer = BucketlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemsViewSet(viewsets.ModelViewSet):
    """Handles Creation and manupulation of Items."""

    queryset = Bucketitems.objects.all()
    serializer_class = BucketitemSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'done')

    def get_queryset(self):
        # Restrict  bucketlist to current user

        queryset = Bucketitems.objects.filter(
            bucketlist_id=self.kwargs['id'],
            bucketlist__creator=self.request.user.id)
        return queryset

    def create(self, request, id=None):
        # Handles the POST request

        request.POST._mutable = True
        request.data['bucketlist'] = self.kwargs['id']
        request.data['done'] = False
        serializer = BucketitemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
