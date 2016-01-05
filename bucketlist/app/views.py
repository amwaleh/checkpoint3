from django.shortcuts import render
from models import Bucketlist, Bucketitems
# Create your views here.
from django.contrib.auth.models import User
from django.http import Http404

from app.serializers import UserSerializer, BucketlistSerializer, BucketitemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

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
		List bucket list and items handle GET and POST request 
	'''
	# Add permission to class
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	
	def get(self, request, format=None):
	    blist = Bucketlist.objects.filter(creator=request.user.id)
	    serializer = BucketlistSerializer(blist, many=True)
	    return Response(serializer.data)

	def post(self, request, format=None):
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
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def get_blist(self, userid, pk):
	    try:
	    	return Bucketlist.objects.get(pk=pk, creator=userid)
	    except Bucketlist.DoesNotExist:
	        raise Http404

	def get(self, request, pk, format=None):
	   	blist = self.get_blist(request.user.id, pk)
		serializer = BucketlistSerializer(blist)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
	    blist = self.get_blist(request.user.id, pk)
	    serializer = BucketlistSerializer(blist, data=request.data)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
	    blist = self.get_blist(request.user.id, pk)
	    blist.delete()
	    return Response(status=status.HTTP_204_NO_CONTENT)

class BucketitemsView(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	
	def check_user(self, pk, userid):
		try: 
			return Bucketlist.objects.get(pk=pk, creator=userid)
		except Bucketlist.DoesNotExist:
			raise Http404
	
	def get_items(self, list_id):
	    try:
	    	return Bucketitems.objects.filter(blist=list_id)
	    except Bucketitems.DoesNotExist:
	        raise Http404

	def get (self, request, pk, format=None):
		self.check_user(pk, request.user.id) 
		item = self.get_items(pk)
		serializer = BucketitemSerializer(item, many=True)
		return Response(serializer.data)

	def post(self, request, pk, format=None):
		self.check_user(pk, request.user.id) 
		request.data['blist'] = pk
		request.data['done'] = False
		serializer = BucketitemSerializer(data=request.data)
		if serializer.is_valid():
		    serializer.save()
		    return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






