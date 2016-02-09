from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Users, Wishes


def index(request):
    return render(request, 'upto/index.html')


def account(request):
    # test with a user
    user_id = '56b8ec3d4303561aa65b05c1'
    user = Users.objects.get(id=user_id)
    context = {
        'one_user': user,
    }
    return render(request, 'upto/myAccount.html', context)


def user_info(request, nom_user):
    user_name = nom_user
    user = Users.objects.get(user__username=user_name)
    context = {
        'user': user,
    }
    return render(request, 'upto/accountDetails.html', context)
