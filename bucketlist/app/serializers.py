from django.contrib.auth.models import User
from models import Bucketitems, Bucketlist
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
	'''
		Serializer for user authenictaion
	'''
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email')

class BuckeitemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bucketitems
		fileds = ('blist', 'name', 'done', 'created_on', 'modified_on')

class BucketlistSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Bucketlist
		fields = ('id','name','created_on', 'modified_on','creator','items')
