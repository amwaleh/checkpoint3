from django.test import TestCase
from django.test import RequestFactory
from django.core.urlresolvers import reverse



class SnippetCreateViewTest(TestCase):
    """
    Test the snippet create view
    """
    def setUp(self): 
    	import ipdb; ipdb.set_trace(
        self.user = UserFactory()
        self.factory = RequestFactory()
    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('login'))
        )
        request.user = self.user
       	
        response = listBucketlists.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['user'], self.user)
        self.assertEqual(response.context_data['request'], request)
