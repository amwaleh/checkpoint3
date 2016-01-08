from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json

domain = 'http://127.0.0.1:8000'

def index(request):
	form = "welcome"
	return render(request, 'index.html', {'form': form})
def login(request):
	if request.method == "GET":
		return render(request, 'signin.html',)

	if request.method == "POST":
		bucketlists = requests.post(domain + '/api/users/')
		form = bucketlists
		return render(request, 'index.html', {'form': form})
	




def listBucketlists(request):
	if request.method == 'GET':
		#import ipdb; ipdb.set_trace()
		bucketlists = requests.get(domain + '/api/bucketlists/')
		lists =bucketlists.json()
		return render(request, 'bucketlist.html', {'lists':lists })
