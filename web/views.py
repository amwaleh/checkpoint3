from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json


domain = 'http://0.0.0.0:8000'
user = {}


def index(request):
    form = "welcome"
    return render(request, 'index.html', {'form': form})


def check_token(request):
    
    if request.session.has_key('Authorization') is False:
        return redirect('/web/login/', )

    data = {'token': request.session['token']}
    verify = requests.post(domain + '/api/api-token-verify/', data)
    if verify.status_code == 200:
        # try to refresh the expired token
        new_token = requests.post(domain + '/api/api-token-refresh/', data)
        new_token = new_token.json()
        if 'token' in new_token:
            token = 'JWT {}'.format(new_token['token'])
            request.session['Authorization'] = token
            return True

        return redirect('/web/login/', )

    return False


def signup(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get('username'),
            "password": request.POST.get('password'),
            "email": request.POST.get('email')
        }
        user = requests.post(domain + '/api/users/', data)
        if user.status_code == 201:
            form = {"info": "Log in"}
            return render(request, 'signin.html', {'form': form})
        form = {"info": user.text}
        return redirect('/web/login/#modal1',)


def login(request):
    if request.method == "GET":
        return render(request, 'signin.html',)

    if request.method == "POST":
        form = {}
        data = {"username": request.POST.get(
            'username'), "password": request.POST.get('password')}
        bucketlists = requests.post(domain + '/api/api-token/', data)
        form = bucketlists.json()
        if 'token' in form:
            token = 'JWT {}'.format(form['token'])
            request.session['Authorization'] = token
            request.session['content_type'] = 'application/json'
            request.session['username'] = request.POST.get('username')
            request.session['token'] = form['token']

            return redirect('/web/bucketlists/', )
        form = {"info": " Wrong password or Username"}
        return render(request, 'signin.html', {'form': form})


def listBucketlists(request):
    if check_token(request) != True:
        return render(request, 'signin.html',)

    if request.method == 'GET':
        # Edit a list
        if 'edit' in request.GET:
            edit_id = request.GET.get('edit')
            edit_list = requests.get(
                domain + '/api/bucketlists/{}/'.format(edit_id), headers=request.session)
            lists = edit_list.json()
            return render(request, 'bucketlist.html', {'lists': lists})
        # Delete bucketlist
        if 'delete' in request.GET:
            delete_id = request.GET.get('delete')
            delete_list = requests.delete(
                domain + '/api/bucketlists/{}/'.format(delete_id), headers=request.session)
        # List all lists
        url = domain + '/api/bucketlists/'
        if 'search' in request.GET:
            search = request.GET.get('search')
            url = domain + '/api/bucketlists/?search={0}'.format(search)
        bucketlists = requests.get(url, headers=request.session)
        lists = bucketlists.json()
        paginator = Paginator(lists, 10)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of
            # results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'bucketlist.html', {'lists': contacts, "header": user})
    if request.method == 'POST':
        # Create a new bucketlist
        name = request.POST.get('name')
        creator = request.user.id
        request.session['content_type'] = 'application/json'
        data = {"name": name, "creator": creator}
        bucketlists = requests.post(
            domain + '/api/bucketlists/', data, headers=request.session)
    return redirect('/web/bucketlists/', )


def listItems(request, id):
    if check_token(request) != True:
        return render(request, 'signin.html',)
    # add an item
    if request.method == 'POST':
        name = request.POST.get('name')
        # Update a Bucketlist
        if 'update' in request.POST:
            url = domain + '/api/bucketlists/{}/'.format(id)
            bucketlists = requests.get(url, headers=request.session)
            bucketlists = bucketlists.json()
            data = bucketlists
            data['name'] = name
            update = requests.put(url, data, headers=request.session)
            return redirect('/web/bucketlists/{}/'.format(id), )
        data = {"name": name}
        item = requests.post(
            domain + '/api/bucketlists/{}/items/'.format(id), data, headers=request.session)
        bucketlists = requests.get(
            domain + '/api/bucketlists/{}/'.format(id), headers=request.session)
        lists = bucketlists.json()
        return render(request, 'list.html', {'key': lists, "header": user})

    if request.method == 'GET':
        bucketlists = requests.get(
            domain + '/api/bucketlists/{}/'.format(id), headers=request.session)
        lists = bucketlists.json()
        return render(request, 'list.html', {'key': lists, "header": user})


def editItems(request, id, item):
    if check_token(request) != True:
        return render(request, 'signin.html',)

    if request.method == 'GET':
        if 'delete' in request.GET:
            delete_list = requests.delete(
                domain + '/api/bucketlists/{0}/items/{1}/'.format(id, item), headers=request.session)
            return redirect('/web/bucketlists/')
        lists = requests.get(
            domain + '/api/bucketlists/{0}/items/{1}/'.format(id, item), headers=request.session)
        lists = lists
        return render(request, 'bucketlist.html', {'lists': lists, "header": user})

    if request.method == 'POST':
        name = request.POST.get('name')
        done = request.POST.get('done')

        if 'update' in request.POST:
            item_res = requests.get(
                domain + "/api/bucketlists/{0}/items/{1}/".format(id, item),  headers=request.session)
            data = item_res.json()
            data['name'] = name
            data['done'] = done
            update = requests.put(
                domain + "/api/bucketlists/{0}/items/{1}/".format(id, item), data, headers=request.session)
            return redirect('/web/bucketlists/{0}/'.format(id))


def logout(request):

    form = ""
    if request.method == 'GET':
        del request.session['Authorization']
        del request.session['username']
        form = "welcome"
        check_token(request)
    return render(request, 'index.html', {'form': form})
