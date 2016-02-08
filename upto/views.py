from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Users, Wishes

def index(request):
    return render(request, 'upto/index.html')

def account(request):
    # test with a user
    user_id = '56b8f12d43035630c76c9360'
    user = Users.objects.get(id=user_id)
    context = {
        'one_user': user,
    }
'''
    WishesNumber = Wishes.document_bases.
    count = {
        'wishesNumber': WishesNumber,
    }'''
    return render(request, 'upto/myAccount.html', context)