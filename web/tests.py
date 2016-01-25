from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Bucketlist, Bucketitems
from django.contrib.auth.models import User
from django.contrib.auth.models import User

factory = APIRequestFactory()

# Create your tests here.


class BucketlistTest(TestCase):
    ''' 
	   Test Views on the Front End 
    '''
    def setUp(self):
    	'''
    	   Setting for test
    	'''
        
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.bucketlist = None
        data = {"username": "admintest", "password": "password"}
        response = self.client.post('/api/users/', data, format='json')
        self.user = User.objects.all().first()
        self.bucketlist = Bucketlist
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_require_login(self):
    	'''
    	   test if login is able
    	'''

        url = '/web/login/'
        data = {"username": "admintest", "password": "password"}
        response = self.client.post(url, data, format='json')
        self.assertContains(response,'signup')
        
        response = self.client.get('/web/')
    def test_homepage(self):
    	'''
    	  testing home page
    	'''
    	response = self.client.get('/web/')
        self.assertEqual(response.status_code, 200)

    def test_bucketlistpage(self):
    	'''
    	  testing main dashboard
    	'''
    	response = self.client.get('/web/bucketlists/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'multiple Lists')

    def test_listpage(self):
    	'''
    	   testing single page dashboad
    	'''
    	response = self.client.get('/web/bucketlists/1/')
        self.assertEqual(response.status_code,200)


       



       
