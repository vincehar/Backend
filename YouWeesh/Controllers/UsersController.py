from operator import methodcaller

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
from YouWeesh.Serializers.GenericSerializer import GenericSerializer
from YouWeesh.Serializers.WishSerializer import WishSerializer
from YouWeesh.Models.Level import Level
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Events import Events
from YouWeesh.Models.Token import Token
from YouWeesh.Models.Wishes import Wishes
from YouWeesh.Models.Preferences import Preferences
from mongoengine.django.auth import User
from YouWeesh.Models.UsersRelationships import UsersRelationships
from mongoengine.django.auth import User
from YouWeesh.Tools.app import App
#from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import ensure_csrf_cookie
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
from datetime import datetime

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes((AllowAny,))
def account(request, _username):
    """
    Get Account information and requests
    :param request:
    :return:
    """
    try:
        connected_user = App.getCurrentUser(request)
        selected_user = Users.objects.get(user__username=_username)
        usersSerializer = UsersSerializer(instance=selected_user)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except selected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(usersSerializer.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getNbrFriends(request):
    try:
        connected_user = Users.objects.get(user__username='marc')
        # TODO : Add criteria for relationship
        nbr = len(UsersRelationships.objects(from_user=connected_user.id))
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(nbr)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getFriends(request):
    try:
        users = Users.objects()
        for u in users:
            print u
        connected_user = Users.objects.get(user__username='marc')
        # TODO : Add criteria for relationship
        lstRelationships = UsersRelationships.objects(from_user=connected_user.id)
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
        #TODO : Select only objects where current user is creator or participant
        lstNextEvents = Events.objects() #user_id=connected_user.id)end_date__lte=datetime.now()) #LTE a changer an SUP
        eventssrz = EventSerializer(instance=lstNextEvents, many=True)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(eventssrz.data)


@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    """
    si on recupere un POST, on essaie de connecter le user
    """
    if request.method == 'POST':
        #username = request.POST['username'].lower();
        #password = request.POST['password']
        username = 'marc'
        password = '123'

        """
        gestion specifique pour les rendering json => mobile
        """
        import json
        #requser = {'username': request.POST.get('username'), 'password': request.POST.get('password')}
        #serializer = BaseUserSerializer(data=requser)
       # data = {}

        user = User.objects.get(username=username)
        users = Users.objects.get(user__username=username)
        userAuth = authenticate(username=username, password=password)
        if user.is_active and user.check_password(password):
            #request.session['UserName'] = user.username
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            usersSerializer = UsersSerializer(instance=users)
            return Response(usersSerializer.data)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createWish(request):

    try:
        _wish_title = request.POST['weesh']
        _idLevel = request.POST['idLevel']

        selectedLevel = Level.objects.get(idLevel=_idLevel)
        connected_user = App.getCurrentUser(request)

        connected_user.create_wish(_wish_title, selectedLevel)

    except selectedLevel.DoesNotExist:
        raise Http404('Level is not existing. Check DB')
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(True)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def updatePosition(request):
    """

    :type request: object
    """
    try:
        _lat = request.POST['lat']
        _lng = request.POST['lng']

        connected_user = App.getCurrentUser(request)
        connected_user.update_position(_lat, _lng)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(True)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allweeshes(request):
    '''

    :return:
    '''
    connected_user = App.getCurrentUser(request)
    if connected_user.preferences.display_weeshes:
        AllWishes = list()
        if connected_user.preferences.selected_network == "PUBLIC":
            AllWishes = Wishes.objects
        if connected_user.preferences.selected_network == "friends":
            for relationship in getFriends(connected_user):
                for wish in Wishes.objects(creator=relationship.from_user.id):
                    AllWishes.append(wish)

        lstWishes = WishSerializer(instance=AllWishes, many=True)
        return Response(lstWishes.data)
    else:
        return None

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allEvents(request):
    '''

    :return:
    '''
    connected_user = App.getCurrentUser(request)
    if connected_user.preferences.display_weeshes:
        AllEvents = list()
        if connected_user.preferences.selected_network == "PUBLIC":
            AllEvents = Events.objects
        if connected_user.preferences.selected_network == "friends":
            for relationship in getFriends(connected_user):
                for wish in Events.objects(creator=relationship.from_user.id):
                    AllEvents.append(wish)

        lstEvents = EventSerializer(instance=AllEvents, many=True)
        return Response(lstEvents.data)
    else:
        return None
'''
@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def weeshesevents(request):
    """
    Get Weeshes And Events sorted by create_date
    :param request:
    :return:
    """
    connected_user = App.getCurrentUser(request)

    ### 1 - manage private and public network ###
    AllEvents = list()
    AllWishes = list()
    if connected_user.preferences.selected_network == "PUBLIC":
        AllEvents = Events.objects
        AllWishes = Wishes.objects
    if connected_user.preferences.selected_network == "friends":
        for relationship in getFriends(connected_user):
            for event in Events.objects(creator=relationship.from_user.id):
                AllEvents.append(event)
            for wish in Wishes.objects(creator=relationship.from_user.id):
                AllWishes.append(wish)
    ### 1                                   #######
    tmplst = list()
    if connected_user.preferences.display_events:
        for event in AllEvents:
            tmplst.append(event)
    if connected_user.preferences.display_weeshes:
        for wish in AllWishes:
            tmplst.append(wish)


    context = sorted(tmplst, key=methodcaller('get_ref_date'), reverse=True)
    lstEvents = EventSerializer(instance=AllEvents, many=True)
    lstWishes = WishSerializer(instance=AllWishes, many=True)
    
    return Response(lstWishes.data)
'''

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def weeshback(request):
    try:
        connected_user = App.getCurrentUser(request)
        current_wish = Wishes.objects.get(id=request.POST['weesh_id'])
        #Atomic update : allow not to have duplicate !
        current_wish.update(add_to_set__weeshback=connected_user)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except current_wish.DoesNotExist:
        raise Http404('Weesh does not exist')
    return Response(True)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def unweeshback(request, _wish_id):
    '''
    Unsubscribe a the connected user to a weeshback
    :param request:
    :param _wish_id:
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        current_wish = Wishes.objects.get(id=_wish_id)
        #Atomic update : allow not to have duplicate !
        current_wish.update(pull__weeshback=connected_user)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except current_wish.DoesNotExist:
        raise Http404('Weesh does not exist')
    return Response(True)