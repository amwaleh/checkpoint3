from django.contrib.auth.models import User
from models import Bucketitems, Bucketlist
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    '''
        Serializer handles User registration signin and signout
    '''
    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BucketitemSerializer(serializers.ModelSerializer):

    ''' serializer Handles items in the bucketlist'''
    class Meta:
        model = Bucketitems
        fileds = ('id', 'blist', 'name', 'done', 'created_on', 'modified_on')


class BucketlistSerializer(serializers.ModelSerializer):

    ''' Serializer Handles Bucketlists '''

    items = BucketitemSerializer(many=True,
                                 required=False,
                                 read_only=True)

    class Meta:
        model = Bucketlist
        fields = (
            'id', 'name', 'created_on', 'modified_on', 'creator', 'items')
