from django.shortcuts import render
from django.conf import settings
import requests

def index(request):
	form = "welcome"
	return render(request, 'index.html', {'form': form})