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

	class Meta:
		ordering = ['-modified_on']

	def __str__(self):
		return self.name


class Bucketitems(models.Model):
	"""
		Model contain bucketitem data
    """
	blist = models.ForeignKey(Bucketlist, related_name='items')
	name = models.CharField(blank=False, max_length=255)
	done = models.BooleanField()
	created_on = models.DateTimeField(auto_now_add=True)
	modified_on = models.DateTimeField(auto_now=True)

	class meta:
		ordering = ['modified_on']

	def __str__(self):
		return self.name
