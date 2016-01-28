from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
import requests
import os

port = int(os.environ.get("PORT", 8000))
domain = 'http://0.0.0.0:{}'.format(port)
user = {}


def index(request):
    form = "welcome"
    return render(request, 'index.html', {'form': form})


def check_token(request):
    # Check if the user is logged in and the token is valid
    if 'Authorization' not in request.session:
        return redirect('/web/login/', )
    data = {'token': request.session['token']}
    verify = requests.post(domain + '/api/api-token-verify/', data)
    # verify if the token is still valid
    if verify.status_code == 200:
        # try to refresh the expired token
        new_token = requests.post(domain + '/api/api-token-refresh/', data)
        new_token = new_token.json()

        if 'token' in new_token:
            token = 'JWT {}'.format(new_token['token'])
            request.session['Authorization'] = token
            return True
        # else if no token was returned
        return redirect('/web/login/', )
        # Token has expired return user to login
    return False


def signup(request):
    # handles signup
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
    # Handles login
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


def list_bucketlists(request):
    # List all bucketlist a user has created
    if check_token(request) is not True:
        return render(request, 'signin.html',)

    if request.method == 'GET':
        # Edit a list
        if 'edit' in request.GET:
            edit_id = request.GET.get('edit')
            edit_list = requests.get(
                domain + '/api/bucketlists/{}/'.format(edit_id),
                headers=request.session)
            lists = edit_list.json()
            return render(request, 'bucketlist.html', {'lists': lists})
        # Delete bucketlist
        if 'delete' in request.GET:
            delete_id = request.GET.get('delete')
            requests.delete(
                domain + '/api/bucketlists/{}/'.format(delete_id),
                headers=request.session)
        # List all lists
        url = domain + '/api/bucketlists/'
        if 'search' in request.GET:
            search = request.GET.get('search')
            url = domain + '/api/bucketlists/?search={0}'.format(search)
        bucketlists = requests.get(url, headers=request.session)
        lists = bucketlists.json()
        paginator = Paginator(lists, 4)
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
        return render(request, 'bucketlist.html',
                      {'lists': contacts,
                       "header": request.session['username']})
    if request.method == 'POST':
        # Create a new bucketlist
        name = request.POST.get('name')
        creator = request.user.id
        request.session['content_type'] = 'application/json'
        data = {"name": name, "creator": creator}
        bucketlists = requests.post(
            domain + '/api/bucketlists/', data,
            headers=request.session)
    return redirect('/web/bucketlists/', )


def list_items(request, id):
    if check_token(request)is not True:
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
            requests.put(url, data, headers=request.session)
            return redirect('/web/bucketlists/{}/'.format(id), )

        data = {"name": name}
        requests.post(
            domain + '/api/bucketlists/{}/items/'.format(id),
            data, headers=request.session)
        bucketlists = requests.get(
            domain + '/api/bucketlists/{}/'.format(id),
            headers=request.session)
        lists = bucketlists.json()
        return render(request, 'list.html',
                      {'key': lists,
                       "header": request.session['username']})

    if request.method == 'GET':
        # List all available lists created by user
        bucketlists = requests.get(
            domain + '/api/bucketlists/{}/'.format(id),
            headers=request.session)
        lists = bucketlists.json()
        return render(request, 'list.html',
                      {'key': lists,
                       "header": request.session['username']})


def edit_items(request, id, item):
    # Handles items within a bucketlist
    if check_token(request) is not True:
        return render(request, 'signin.html',)

    if request.method == 'GET':
        if 'delete' in request.GET:
            # perform delete request of an item
            requests.delete(
                domain + '/api/bucketlists/{0}/items/{1}/'.format(id, item),
                headers=request.session)
            return redirect('/web/bucketlists/')
        lists = requests.get(
            domain + '/api/bucketlists/{0}/items/{1}/'.format(id, item),
            headers=request.session)
        lists = lists
        return render(request, 'bucketlist.html',
                      {'lists': lists, "header": request.session['username']})

    if request.method == 'POST':
        # Handles the creation of a new item to a list
        name = request.POST.get('name')
        done = request.POST.get('done')
        if 'update' in request.POST:
            # update the information contained in an item
            item_res = requests.get(
                domain + "/api/bucketlists/{0}/items/{1}/".format(id, item),
                headers=request.session)
            data = item_res.json()
            data['name'] = name
            data['done'] = done
            requests.put(
                domain + "/api/bucketlists/{0}/items/{1}/".format(id, item),
                data, headers=request.session)
            return redirect('/web/bucketlists/{0}/'.format(id))


def logout(request):
    # logs out a user from the system
    form = ""
    if request.method == 'GET':
        del request.session['Authorization']
        del request.session['username']
        form = "welcome"
        check_token(request)
    return render(request, 'index.html', {'form': form})
