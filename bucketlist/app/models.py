from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Bucketlist(models.Model):
	"""
	 	Model contains Buckelist data
    """
	name = models.CharField(blank=False, max_length=255)
	creator = models.ForeignKey(User)
	created_on = models.DateTimeField(auto_now_add=True)
	modified_on = models.DateTimeField(auto_now=True)

class Bucketitems(models.Model):
	"""
		Model contain bucketitem data
    """
	blist = models.ForeignKey(Bucketlist)
	name = models.CharField(blank=False, max_length=255)
	done = models.BooleanField()
	created_on = models.DateTimeField(auto_now_add=True)
	modified_on = models.DateTimeField(auto_now=True)
