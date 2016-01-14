from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json


domain = 'http://127.0.0.1:8000'

headers = {}


def index(request):
	form = "welcome"
	return render(request, 'index.html', {'form': form})

def login(request):

	
	if request.method == "GET":
		return render(request, 'signin.html',)

	if request.method == "POST":

		form={}
		data={"username":request.POST.get('username'), "password":request.POST.get('password')}
		bucketlists = requests.post(domain + '/api/api-token/',data)
		form = bucketlists.json()
		if 'token' in form :
			token = 'token {}'.format(form['token'])
			headers['Authorization'] = token
			return redirect('/web/bucketlists/', )
		
		form = {"info":" Wrong password or Username"}

		return render(request,'signin.html', {'form': form})
	
def listBucketlists(request):
	if headers == {}:
		return redirect('/web/login/', )

	if request.method == 'GET':
		
		bucketlists = requests.get(domain + '/api/bucketlists/',headers=headers)
		lists = bucketlists.json()
		return render(request, 'bucketlist.html', {'lists':lists})

	if request.method == 'POST':
	
		name = request.POST.get('name')
		creator = request.user.id
		headers['content_type'] = 'application/json'
		data = {"name":name, "creator":creator}
		bucketlists = requests.post(domain + '/api/bucketlists/', data, headers=headers)

	return redirect('/web/bucketlists/', )



