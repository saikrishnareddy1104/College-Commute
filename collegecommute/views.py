from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
def home(request):
 return render(request,'commutehome.html')

