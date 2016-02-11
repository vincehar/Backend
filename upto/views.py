from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Users, Wishes, Events

def index(request):
    return render(request, 'upto/index.html')

def account(request):
    # test with a user
    user_id = Users.objects.get(user__username='marc').id
    user = Users.objects.get(id=user_id)
    context = {
        'one_user': user,
    }
    return render(request, 'upto/myaccount.html', context)

def user_info(request, nom_user):
    user_name = nom_user
    user = Users.objects.get(user__username=user_name)
    context = {
        'user': user,
    }
    return render(request, 'upto/accountDetails.html', context)

def allwishesAndEvent(request):

    w = Users.objects.order_by('events_Owned.start_date')#.only('wishes')
    w = Users.objects.order_by('events_Owned.start_date')
    context = {
        'wishes': w,
    }
    return render(request, 'upto/wishes.html', context)