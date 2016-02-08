from django.shortcuts import render
from django.http import Http404
from .models import Users

def index(request):
    return render(request, 'upto/index.html')

def account(request):
    #try
    context = Users.objects().first()
    print context.username
    #return render(request, 'upto/myAccount.html', context)
    '''except Users
    '''