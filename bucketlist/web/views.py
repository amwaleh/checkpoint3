from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json


domain = 'http://127.0.0.1:8000'
headers = {}

def check_auth(self):
	if headers == {}:
		return redirect('/web/login/', )

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
			headers['content_type'] = 'application/json'
			return redirect('/web/bucketlists/', )
		
		form = {"info":" Wrong password or Username"}

		return render(request,'signin.html', {'form': form})
	
def listBucketlists(request):
	if headers == {}:
		return redirect('/web/login/', )
	

	if request.method == 'GET':
		
		if 'edit' in request.GET :
			edit_id = request.GET.get('edit')
			edit_list = requests.get(domain + '/api/bucketlists/{}/'.format(edit_id),headers=headers)
			lists = edit_list.json()
			return render(request, 'bucketlist.html', {'lists':lists})
		# Delete bucketlist
		if 'delete' in request.GET :
			delete_id = request.GET.get('delete')
			delete_list = requests.delete(domain + '/api/bucketlists/{}/'.format(delete_id),headers=headers)
		bucketlists = requests.get(domain + '/api/bucketlists/',headers=headers)
		lists = bucketlists.json()
		paginator = Paginator(lists, 10)
		page = request.GET.get('page')
		
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		return render(request, 'bucketlist.html', {'lists':contacts})

	if request.method == 'POST':
		name = request.POST.get('name')
		creator = request.user.id
		headers['content_type'] = 'application/json'
		data = {"name":name, "creator":creator}
		bucketlists = requests.post(domain + '/api/bucketlists/', data, headers=headers)
	return redirect('/web/bucketlists/', )

def listItems(request,id):
	if headers == {}:
		return redirect('/web/login/', )
	#add an item
	if request.method == 'POST':
		name = request.POST.get('name')
		# Update a Bucketlist
		if 'update' in request.POST :
			bucketlists = requests.get(domain + '/api/bucketlists/{}/'.format(id),headers=headers)
			bucketlists = bucketlists.json()
			data = bucketlists
			data['name'] = name
			update = requests.put(domain + '/api/bucketlists/{}/'.format(id), data, headers=headers)
			return redirect('/web/bucketlists/{}/'.format(id), )

		data = {"name":name}
		item = requests.post(domain + '/api/bucketlists/{}/items/'.format(id), data, headers=headers)
		bucketlists = requests.get(domain + '/api/bucketlists/{}/'.format(id),headers=headers)
		lists = bucketlists.json()
		return render(request, 'list.html', {'key':lists})

	if request.method == 'GET':
		bucketlists = requests.get(domain + '/api/bucketlists/{}/'.format(id),headers=headers)
		lists = bucketlists.json()
		return render(request, 'list.html', {'key':lists})

def editItems(request,id,item):
	
	if headers == {}:
		return redirect('/web/login/', )

	if request.method == 'GET':
		if 'delete' in request.GET:
			delete_list = requests.delete(domain + '/api/bucketlists/{0}/items/{1}/'.format(id,item),headers=headers)
			return redirect('/web/bucketlists/' )
		lists = requests.get(domain + '/api/bucketlists/{0}/items/{1}/'.format(id,item),headers=headers)
		lists = lists
		return render(request, 'bucketlist.html', {'lists':lists})

	if request.method == 'POST':
		name = request.POST.get('name')
		done = request.POST.get('done')

		if 'update' in request.POST :
			item_res = requests.get(domain + "/api/bucketlists/{}/items/{}/".format(id,item),  headers=headers)
			data = item_res.json()
			data['name'] = name
			data['done'] = done
			update = requests.put(domain + "/api/bucketlists/{}/items/{}/".format(id,item), data, headers=headers)
			return redirect('/web/bucketlists/{}/'.format(id ))





