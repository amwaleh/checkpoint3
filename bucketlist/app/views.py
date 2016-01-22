
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from models import Bucketlist, Bucketitems
from serializers import UserSerializer, BucketlistSerializer, BucketitemSerializer

class StandardResultsSetPagination(PageNumberPagination):
	django_paginator_class ='django.core.paginator.Paginator'
	page_size = 1
	paginate_by_param = 'page_size'
	max_page_size = 2

class UserList(APIView):

    """
            List all users, or create a new user.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Bucketlists(APIView):
    '''
            List bucket list and items handle GET and POST request 
    '''
    # Add permission to class
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
    
        blist = Bucketlist.objects.filter(creator=request.user.id)
        if 'search' in request.GET:
            search =request.GET.get('search')
            blist = blist.filter(name__icontains=search)

        serializer = BucketlistSerializer(blist, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.POST._mutable=True
        request.data['creator'] = request.user.id
        serializer = BucketlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditBucketlists(APIView):

    '''
            List bucket list and items handle GET and POST request 
    '''
    # Add permissiion to class
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
  

    def get_blist(self, userid, id):
        # Checks if Buckelist exists
        try:
            return Bucketlist.objects.get(id=id, creator=userid)
        except Bucketlist.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
            # handles the GEt request
        blist = self.get_blist(request.user.id, id)
        serializer = BucketlistSerializer(blist)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        # Handles PUT Request
        blist = self.get_blist(request.user.id, id)
        serializer = BucketlistSerializer(blist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
            # Handles Delete Request
        blist = self.get_blist(request.user.id, id)
        blist.delete()
        return Response({"info":"List Deleted"},status=status.HTTP_204_NO_CONTENT)


class BucketitemsView(APIView):

    '''
            Handles POST and GET request for Editing bucketlist items
    '''
    # Token and user login permissions
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def check_user(self, id, userid):
            # Check if the logged in user is the creator of the the list
        try:
            return Bucketlist.objects.get(id=id, creator=userid)
        except Bucketlist.DoesNotExist:
            raise Http404

    def get_items(self, list_id):
        # Check if the item exists
        try:
            return Bucketitems.objects.filter(blist=list_id)
        except Bucketitems.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
            # Handles the GET request
        self.check_user(id, request.user.id)
        item = self.get_items(id)
        serializer = BucketitemSerializer(item, many=True)
        re#turn Response(serializer.data)

    def post(self, request, id, format=None):
        # Handles the POST request
     
        self.check_user(id, request.user.id)
        request.POST._mutable=True
        request.data['blist'] = id
        request.data['done'] = False
        serializer = BucketitemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditBucketitemsView(APIView):

    '''
            Handles PUT and DELETE request for Editing an item in a Bucketlist
    '''
    # Token and user login permissions
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def check_user(self, id, userid):
        try:
            return Bucketlist.objects.get(id=id, creator=userid)
        except Bucketlist.DoesNotExist:
            raise Http404

    def get_items(self, list_id, item_id):
        try:
            return Bucketitems.objects.get(blist=list_id, id=item_id)
        except Bucketitems.DoesNotExist:
            raise Http404

    def get(self, request, id, item_id, format=None):
        self.check_user(id, request.user.id)
        item = self.get_items(id, item_id)
        serializer = BucketitemSerializer(item)
        return Response(serializer.data)

    def put(self, request, id, item_id, format=None):
        self.check_user(id, request.user.id)
        item = self.get_items(id, item_id)
       
        serializer = BucketitemSerializer(item, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, item_id, format=None):
        self.check_user(id, request.user.id)
        item = self.get_items(id, item_id)
        item.delete()
        return Response('Item Deleted',status=status.HTTP_204_NO_CONTENT)
