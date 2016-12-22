from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core import serializers as djangoSerializers
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Serializers.EventSerializer import EventSerializer
from YouWeesh.Models.Level import Level
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Events import Events
from YouWeesh.Models.Token import Token
from mongoengine.django.auth import User
from YouWeesh.Models.UsersRelationships import UsersRelationships
from mongoengine.django.auth import User
#from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import ensure_csrf_cookie
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
from datetime import datetime

def getConnectedUser(request):
        return Users.objects.get(user__username='marc')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes((AllowAny,))
def account(request):
    """
    Get Account information and requests
    :param request:
    :return:
    """
    try:
        connected_user = getConnectedUser(request)
        #friends_requests = UsersRelationships.objects(accepted=False, to_user=connected_user.id) #UsersRelationships.objects.get(to_user=connected_user.id)
        #my_friends = UsersRelationships.objects(accepted=True, to_user=connected_user.id)
        usersSerializer = UsersSerializer(instance=connected_user)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(usersSerializer.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getNbrFriends(request):
    try:
        connected_user = Users.objects.get(user__username='marc')
        # TODO : Add criteria for relationship
        nbr = len(UsersRelationships.objects())
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(nbr)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getFriends(request):
    try:

        connected_user = Users.objects.get(user__username='marc')
        # TODO : Add criteria for relationship
        lstRelationships = UsersRelationships.objects()
        lstFriends = list()
        for rl in lstRelationships:
            lstFriends.append(rl.to_user)
        usersSerializer = UsersSerializer(instance=lstFriends, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(usersSerializer.data)
'''
@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getTags(request):
    try:
        connected_user = Users.objects.get(user__username='marc')
'''
@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def myNextEvents(request):
    try:
        connected_user = Users.objects.get(user__username='marc')
        lstNextEvents = Events.objects() #user_id=connected_user.id)end_date__lte=datetime.now()) #LTE a changer an SUP
        eventssrz = EventSerializer(instance=lstNextEvents, many=True)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(eventssrz.data)
        return Response(events.data)


@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createWish(request):

    try:
        _wish_title = request.POST['weesh']
        _idLevel = request.POST['idLevel']

        selectedLevel = Level.objects.get(idLevel=_idLevel)
        connected_user = getConnectedUser(request)

        connected_user.create_wish(_wish_title, selectedLevel)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(True)
