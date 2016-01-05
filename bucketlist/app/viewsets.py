from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from models import Bucketlist, Bucketitems
# Create your views here.
from django.contrib.auth.models import User
from django.http import Http404

from app.serializers import UserSerializer, BucketlistSerializer, BucketitemSerializer
from rest_framework.views import APIView

from rest_framework import status
from rest_framework import permissions


class BucketlistViewset(viewsets.ModelViewSet):

	queryset = Bucketlist.objects.all()
	serializer_class = BucketlistSerializer
	permission_classes = (permissions.IsAuthenticated,)

	