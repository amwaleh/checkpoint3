from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages
from django.core.urlresolvers import reverse
import requests
import os


PORT = int(os.environ.get("PORT", 8000))
DOMAIN = 'http://0.0.0.0:{}'.format(PORT)




def login_required(handler):
    """Handle Authenication."""
    def check_login(self, *args, **kwargs):
        if 'Authorization' not in self.request.session:
            return redirect(reverse('login'), abort=False)
        data = {'token': self.request.session['token']}
        verify = requests.post(DOMAIN + '/api/api-token-verify/', data)
        # verify if the token is still valid
        if verify.status_code == 200:
            return handler(self, *args, **kwargs)
        # else if no token was returned
        return redirect(reverse('login'), abort=False)
    # Token has expired return user to login
    return check_login


class Welcome(View):
    """Handle Welcome Screen."""

    def get(self, request):
        # show slider
        return render(request, 'index.html')


class Signup(View):
    """handle signup."""

    def post(self, request, *args, **kwargs):
        # handles signup
        data = {
            "username": request.POST.get('username'),
            "password": request.POST.get('password'),
            "email": request.POST.get('email')}
        user = requests.post(DOMAIN + '/api/users/', data)
        if user.status_code == 201:
            messages.success(request, 'Signup success. Login now')
            form = {"info": "Log in"}
            return render(request, 'signin.html', {'form': form})
        form = {"info": user.text}
        messages.error(request, user.text)
        return redirect(reverse('login'),)


class Login(View):
    """Handles login."""

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
            messages.success(request, 'login success')
            return redirect(reverse('detail'))
        form = {"info": " Wrong password or Username"}
        return render(request, 'signin.html', {'form': form})


class ListCreateBucketlists(View):
    """Lists all bucketlist a user has created."""

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
        messages.success(request, 'List created')
        return redirect(reverse('detail'),)


class DeleteList(View):
    """Deletes bucketlist."""

    # Delete bucketlist '/bucketlis/{}/delete'
    @login_required
    def post(self, request, id=None):
        url = DOMAIN + '/api/bucketlists/{}/'.format(id)
        requests.delete(url, headers=request.session)
        messages.success(request, 'List deleted')
        return redirect(reverse('detail'), )


class UpdateList(View):
    """Updates  bucketlist"""

    @login_required
    def post(self, request, id=None):
        name = request.POST.get('name')
        url = DOMAIN + '/api/bucketlists/{}/'.format(id)
        bucketlist = requests.get(url, headers=request.session)
        update_data = bucketlist.json()
        update_data['name'] = name
        requests.put(url, update_data, headers=request.session)
        messages.success(request, 'List updated')
        return redirect(reverse('detail'))


class CreateListItems(View):
    """handles Creation and listing of items."""

    @login_required
    def get(self, request, id=None):
        # handles listing of items
        url = DOMAIN + '/api/bucketlists/{}/'.format(id)
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
        messages.success(request, 'item created')
        result_url = DOMAIN + '/api/bucketlists/{}/'.format(id)
        bucketlist = requests.get(result_url, headers=request.session)
        list_items = bucketlist.json()
        return render(request, 'list.html',
                      {'key': list_items,
                       "header": request.session['username']})


class DeleteItem(View):
    """Handles  Deletion of an item."""

    # Update bucketlist '/bucketlis/{}/item/{}/delete'
    @login_required
    def post(self, request, id=None, item=None):
        # Delete an item
        url = DOMAIN + '/api/bucketlists/{0}/items/{1}/'.format(id, item)
        requests.delete(url, headers=request.session)
        messages.success(request, 'item Deleted')
        return redirect(reverse('detail'))


class UpdateItem(View):
    """Handles Deletion of Item"""

    # Update bucketlist '/bucketlist/{}/item/{}/update'
    @login_required
    def post(self, request, id=None, item=None):
        # update edits made to an item

        done = False
        name = request.POST.get('name')
        res_done = request.POST.get('done')
        if res_done == 'on':
            done = True
        url = DOMAIN + "/api/bucketlists/{0}/items/{1}/".format(id, item)
        item_details = requests.get(url, headers=request.session)
        data = item_details.json()
        data['name'] = name
        data['done'] = done
        requests.put(url, data, headers=request.session)
        messages.success(request, 'item updated')
        return redirect(reverse('items', args=[id]))

    def get(self, request, id=None, item=None):
        return redirect(reverse('items', args=[id]))


class Logout(View):
    """logs out a user from the system"""

    @login_required
    def get(self, request):
        del request.session['Authorization']
        del request.session['username']
        messages.success(request, 'You have been logged out')
        return render(request, 'index.html')


class SearchView(View):
    """handles Search Query"""

    @login_required
    def post(self, request):
        search = request.POST.get('search')
        url = DOMAIN + "/api/bucketlists?search={}".format(search)
        bucketlists = requests.get(url, headers=request.session)
        lists = bucketlists.json()
        paginator = Paginator(lists, 5)
        page = request.GET.get('page')
        try:
            buckets = paginator.page(page)
        except PageNotAnInteger:
            buckets = paginator.page(1)
        except EmptyPage:
            buckets = paginator.page(paginator.num_pages)
        return render(request, 'bucketlist.html',
                      {'lists': buckets,
                       'search': search,
                       "header": request.session['username']})

    @login_required
    def get(self, request):
        return redirect(reverse('detail'))
