from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Bucketlist, Bucketitems
from django.contrib.auth.models import User


factory = APIRequestFactory()

# Create your tests here.

class BucketlistTest(APITestCase):
	@classmethod
	def SetUp(self):
		url = '/users/'
		data = {"username": "admintest", "password":"password"}
		
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.get().username, 'admintest')
		self.assertEqual(User.objects.count(), 1)


	def test_1_create_account(self):

		"""
			Ensure we can create a new account object.
		"""
		url = '/users/'
		data = {"username": "admintest", "password":"password"}
		
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.get().username, 'admintest')
		self.assertEqual(User.objects.count(), 1)

	def test_2_Authorization(self):
		url = '/api-token'
		data = {"username": "admintest", "password":"password"}
		response = self.client.post(url, data, format='json')
		print response.data
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(response.status_code, 200)

        # need to check how passwords are saved