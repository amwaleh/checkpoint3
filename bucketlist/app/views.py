from django.shortcuts import render
from models import Bucketlist, Bucketitems
# Create your views here.
from django.contrib.auth.models import User
from django.http import Http404

from app.serializers import UserSerializer, BucketlistSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserList(APIView):
	"""
		List all users, or create a new user.
	"""
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
		List bucket list and items
	'''
	def get(self, request, format=None):
	    blist = Bucketlist.objects.all()
	    serializer = BucketlistSerializer(blist, many=True)
	    return Response(serializer.data)

	def post(self, request, format=None):
	    serializer = BucketlistSerializer(data=request.data)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data, status=status.HTTP_201_CREATED)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditBucketlists(APIView):

	def get_blist(self, pk):
	    try:
	    	return Bucketlist.objects.get(pk=pk)
	    except Bucketlist.DoesNotExist:
	        raise Http404

	def get(self, request, pk, format=None):
	   	blist = self.get_blist(pk)
		# blist = Bucketlist.objects.get(pk)
		serializer = BucketlistSerializer(blist)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
	    blist = self.get_blist(pk)
	    serializer = BucketlistSerializer(blist, data=request.data)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
	    blist = self.get_blist(pk)
	    blist.delete()
	    return Response(status=status.HTTP_204_NO_CONTENT)

class BucketitemsView(APIView):
	def get_items(self, pk):
	    try:
	    	return Bucketitems.objects.get(pk=pk)
	    except Bucketlist.DoesNotExist:
	        raise Http404
	def get (self,request,pk, item_id, format=None):
		item = self.get_items(item_id)