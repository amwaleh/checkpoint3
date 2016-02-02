from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.generic import View
import requests
import os


PORT = int(os.environ.get("PORT", 8000))
DOMAIN = 'http://0.0.0.0:{}'.format(PORT)
user = {}
LOGIN_REDIRECT_URL = '/login'


def login_required(handler):
    """  Handles Authenication """

    def check_login(self, *args, **kwargs):
        if 'Authorization' not in self.request.session:
            return redirect('/web/login/', abort=False)
        data = {'token': self.request.session['token']}
        verify = requests.post(DOMAIN + '/api/api-token-verify/', data)
        # verify if the token is still valid
        # Refresh the token
        if verify.status_code == 200:
            token_data = requests.post(
                DOMAIN + '/api/api-token-refresh/', data)
            new_token = token_data.json()
            if 'token' in new_token:
                token = 'JWT {}'.format(new_token['token'])
                self.request.session['Authorization'] = token
                return handler(self, *args, **kwargs)
            # else if no token was returned
        return redirect('/web/login/', abort=False)
        # Token has expired return user to login
    return check_login


class Welcome(View):

    """ Handles Welcome Screen """

    def get(self, request):
        return render(request, 'index.html')


class Signup(View):

    """handles signup"""

    def post(self, request, *args, **kwargs):
        data = {
            "username": request.POST.get('username'),
            "password": request.POST.get('password'),
            "email": request.POST.get('email')}
        user = requests.post(DOMAIN + '/api/users/', data)
        if user.status_code == 201:
            form = {"info": "Log in"}
            return render(request, 'signin.html', {'form': form})
        form = {"info": user.text}
        return redirect('/web/login/#modal1',)


class Login(View):

    """Handles login"""

    def get(self, request):
        return render(request, 'signin.html',)

    def post(self, request, *args, **kwargs):
        form = {}
        data = {"username": request.POST.get(
            'username'), "password": request.POST.get('password')}
        bucketlists = requests.post(DOMAIN + '/api/api-token/', data)
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


class ListCreateBucketlists(View):

    """Lists all bucketlist a user has created"""

    @login_required
    def get(self, request):

        url = DOMAIN + '/api/bucketlists/'
        bucketlists = requests.get(url, headers=request.session)
        lists = bucketlists.json()
        paginator = Paginator(lists, 4)
        page = request.GET.get('page')
        try:
            buckets = paginator.page(page)
        except PageNotAnInteger:
            buckets = paginator.page(1)
        except EmptyPage:
            buckets = paginator.page(paginator.num_pages)
        return render(request, 'bucketlist.html',
                      {'lists': buckets,
                       "header": request.session['username']})

    @login_required
    def post(self, request):
        # Create a new bucketlist
        name = request.POST.get('name')
        creator = request.user.id
        request.session['content_type'] = 'application/json'
        url = DOMAIN + '/api/bucketlists/'
        data = {"name": name, "creator": creator}
        requests.post(url, data, headers=request.session)
        return redirect('/web/bucketlists/', )


class DeleteList(View):

    """  Deletes bucketlist"""

    # Delete bucketlist '/bucketlis/{}/delete'
    @login_required
    def post(self, request, id=None):
        url = DOMAIN + '/api/bucketlists/{}/'.format(id)
        requests.delete(url, headers=request.session)
        return redirect('/web/bucketlists/', )


class UpdateList(View):

    """ Updates  bucketlist"""
    # Update bucketlist '/bucketlis/{}/update'
    @login_required
    def post(self, request, id=None):
        name = request.POST.get('name')
        url = DOMAIN + '/api/bucketlists/{}/'.format(id)
        bucketlist = requests.get(url, headers=request.session)
        update_data = bucketlist.json()
        update_data['name'] = name
        requests.put(url, update_data, headers=request.session)
        return redirect('/web/bucketlists/{}/'.format(id), )


class CreateListItems(View):

    """ handles Creation and listing of items """
    @login_required
    def get(self, request, id=None):
        # handles listing of items
        url = DOMAIN + '/api/bucketlists/{}/items'.format(id)
        bucketlists = requests.get(url, headers=request.session)
        lists = bucketlists.json()
        return render(request, 'list.html',
                      {'key': lists,
                       "header": request.session['username']})

    @login_required
    def post(self, request, id=None):
        # Handles creation of items
        name = request.POST.get('name')
        data = {"name": name}
        url = DOMAIN + '/api/bucketlists/{}/items/'.format(id)
        requests.post(url, data, headers=request.session)
        result_url = DOMAIN + '/api/bucketlists/{}/'.format(id)
        bucketlist = requests.get(result_url, headers=request.session)
        list_items = bucketlist.json()
        return render(request, 'list.html',
                      {'key': list_items,
                       "header": request.session['username']})


class DeleteItem(View):

    """ Handles  Deletion of an item """
    # Update bucketlist '/bucketlis/{}/item/{}/delete'
    @login_required
    def post(self, request, id=None, item=None):
        # Delete an item
        url = DOMAIN + '/api/bucketlists/{0}/items/{1}/'.format(id, item)
        requests.delete(url, headers=request.session)
        return redirect('/web/bucketlists/')


class UpdateItem(View):

    """ Handles Deletion of Item """
    # Update bucketlist '/bucketlis/{}/item/{}/update'
    @login_required
    def post(self, request, id=None, item=None):
        # update edits made to an item
        name = request.POST.get('name')
        done = request.POST.get('done')
        url = DOMAIN + "/api/bucketlists/{0}/items/{1}/".format(id, item)
        item_details = requests.get(url, headers=request.session)
        data = item_details.json()
        data['name'] = name
        data['done'] = done
        requests.put(url, data, headers=request.session)
        return redirect('/web/bucketlists/{0}/'.format(id))


class Logout(View):

    """logs out a user from the system"""
    @login_required
    def get(self, request):
        try:
            del request.session['Authorization']
            del request.session['username']
            return render(request, 'index.html')
        except:
            return render(request, 'index.html')
            # handles an attempt to logout session is available


class SearchView(View):

    """ handles Search Query """

    @login_required
    def post(self, request):
        search = request.POST.get('search')
        url = DOMAIN + "/api/bucketlists?search={}".format(search)
        bucketlists = requests.get(url, headers=request.session)
        lists = bucketlists.json()
        paginator = Paginator(lists, 4)
        page = request.GET.get('page')
        try:
            buckets = paginator.page(page)
        except PageNotAnInteger:
            buckets = paginator.page(1)
        except EmptyPage:
            buckets = paginator.page(paginator.num_pages)
        return render(request, 'bucketlist.html',
                      {'lists': buckets,
                       "header": request.session['username']})
