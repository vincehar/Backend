from django.shortcuts import render
from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseRedirect
from mongoengine.queryset.visitor  import Q
from .models import Users, Wishes, Events, UsersRelationships
from serializers import UsersSerializer, UsersRelationShipsSerializer, BaseUserSerializer, WishSerializer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import redirect
from itertools import chain
from operator import itemgetter, attrgetter, methodcaller
from collections import defaultdict
import datetime
from django.contrib.auth import login as log, authenticate
#from regme.documents import User
from mongoengine.django.auth import User
from upto.forms import UsersLoginForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt

def index(request):
    return render(request, 'upto/index.html')

@ensure_csrf_cookie
@api_view(('GET', 'POST'))
@permission_classes((AllowAny, ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    from mongoengine.queryset import DoesNotExist
    """
    si on recupere un POST, on essaie de connecter le user
    """
    if request.method == 'POST':
        """
        recuperation des donnees du POST
        """
        username = request.POST['username']
        password = request.POST['password']
        """
        gestion specifique pour les rendering HTML => desktop
        """
        if request.accepted_renderer.format == 'html':
            form = UsersLoginForm(request, data=request.POST)
            try:
                if form.is_valid():
                    user = User.objects.get(username=username)
                    user = authenticate(username=username, password=password)
                    if user.is_active and user.check_password(password):
                        user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                        request.session.set_expiry(60 * 60 * 1)
                        #return HttpResponse(json.dumps({'user':'connected'}))
                        #return allwishesAndEvent(request)
                        return HttpResponseRedirect('/upto/wishes/')
                else:
                    return render(request, 'registration/login.html', {'form': form})
            except DoesNotExist:
                return HttpResponseRedirect('/upto/account/register/')
                #return HttpResponse(json.dumps({'user':'not exists'}))

        """
        gestion specifique pour les rendering json => mobile
        """
        import json
        requser = {'username': request.POST.get('username'), 'password': request.POST.get('password')}
        serializer = BaseUserSerializer(data=requser)
        data = {}
        try:
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user.is_active and user.check_password(password):
                request.session['UserName'] = user.username
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                data['result'] = 'success'
                data['username'] = username
            else:
                print("no log")
                data['result'] = 'failed'
                data['username'] = 'please log in'
        except DoesNotExist:
            data['result'] = 'does not exist'
            data['username'] = 'please register'
        return HttpResponse(json.dumps(data), content_type = "application/json")

    else:
        form = UsersLoginForm()
        return render(request, 'registration/login.html', {'form': form})


@permission_classes((IsAuthenticated, ))
def account(request):
    # test with a user
    user_id = Users.objects.get(user__username='marc').id
    user = Users.objects.get(id=user_id)
    context = {
        'one_user': user,
    }
    return render(request, 'upto/myaccount.html', context)

@api_view(('GET',))
@permission_classes((AllowAny, ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def userdetails(request, username):

    user = Users.objects.get(user__username=username)
    relationShips = UsersRelationships.objects(Q(from_user=user) | Q(to_user=user))

    context = {
            'user': user,
            'relationShips': relationShips
    }
    if request.accepted_renderer.format == 'html':
        return render(request, 'upto/userdetails.html', context)

    userSerializer = UsersSerializer(instance=user)
    relationShipsSerializer = UsersRelationShipsSerializer(instance=relationShips, many=True)

    return Response({'user': userSerializer.data, 'relationShips': relationShipsSerializer.data})

@permission_classes((IsAuthenticated, ))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allwishesAndEvent(request):

    if request.method == 'POST':
        request.session['username'] = request.POST['username']
    tmplst = list()
    request.session['username'] = 'ceika'
    for event in Events.objects:
        tmplst.append(event)
    for wish in Wishes.objects:
        tmplst.append(wish)
    context = {
        'eventsList': sorted(tmplst, key=methodcaller('get_ref_date'), reverse=True),
        'username': request.session['username'],
    }

    #if request.accepted_renderer.format == 'html':
    if 1==1:
        return render(request, 'upto/wishes.html', context)
    else:
        serializer = WishSerializer(instance=context)
        data = serializer.data
        return Response(data)

def getEventInfo(request, _event_id):
    event = Events.objects.get(id=_event_id)
    current_user = Users.objects.get(user__username=request.session['username'])
    print _event_id
    context = {
        'currentEvent': event,
        'current_user': current_user,
    }

    return render(request, 'upto/eventDetails.html', context)

@csrf_exempt
@permission_classes((IsAuthenticated, ))
def createWish(request, username):
    """
    View used to create a wish for a user
    :rtype: object
    :param _id_user:
    :param request:
    """
    #1 - get user with id
    current_user = Users.objects.get(user__username=request.session['username'])

    #2 - get wish title from form
    _wish_title = request.POST['wish']
    current_user.create_wish(_wish_title)

    return redirect('/upto/wishes/')

def deleteWish(request, _wish_id):
    """
    Used to delete wish with a wish ID
    :param request:
    :param _wish_id:
    :return:
    """
    try:
        Wishes.delete(Wishes.objects.get(id=_wish_id))
    except Wishes.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return redirect('/upto/wishes/')

def createEvent(request):
    """
    View used to create a wish for a user
    :rtype: object
    :param _id_user:
    :param request:
    """
    try:
        #1 - get event_id
        #name = 'marc'
        current_user = Users.objects.get(id=request.POST['user_id'])
        #2 - get wish title from form
        eventName = request.POST['eventName']

        start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d %H:%M")
        end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d %H:%M")

        current_user.create_event(eventName, start_date, end_date)
    except Users.DoesNotExist:
        raise Http404('Event id does not exist')
    else:
        return redirect('/upto/wishes/')

def deleteEvent(request, _event_id):
    """
    Used to delete an event with an event ID
    :param _event_id:
    :return:
    """
    try:
        Events.delete(Events.objects.get(id=_event_id))
    except Wishes.DoesNotExist:
        raise Http404('Event id does not exist')
    else:
        return redirect('/upto/wishes/')