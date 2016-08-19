from django.contrib.auth.models import User
from models import Bucketitems, Bucketlist
from rest_framework import serializers
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):

    """Serializer handles User registration signin and signout."""
    password = serializers.CharField(style={'input_type':'password'}, required=False, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        # override create function to save password
        #JWT uses harshed password

        if 'password' in validated_data and validated_data['password']:
            user = User.objects.create(username=validated_data['username'])
            user.set_password(validated_data['password'])
            user.save()
            return user
        raise serializers.ValidationError('Error:password cannot be empty')
        return validated_data

    def update(self, instance, validated_data):
        # call set_password on user object. Without this
        # the password will be stored in plain text.

        instance.username = validated_data.get('username', instance.username)
        if check_password(validated_data.get('password'), instance.password):
            print('password same')

        instance.set_password(validated_data.get(instance.password))
        instance.save()
        return instance



class BucketitemSerializer(serializers.ModelSerializer):

    """serializer Handles items in the bucketlist"""

    class Meta:
        model = Bucketitems
        fileds = ('url', 'bucketlist', 'name', 'done', 'created_on',
                  'modified_on')


class BucketlistSerializer(serializers.ModelSerializer):

    """ Serializer Handles Bucketlists """

    items = BucketitemSerializer(many=True,
                                 required=False,
                                 read_only=True)

    class Meta:
        model = Bucketlist
        fields = (
            'id', 'name', 'created_on',
            'modified_on', 'creator', 'items')

