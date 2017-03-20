from operator import methodcaller
from collections import Counter
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core import serializers as djangoSerializers
from django.core.exceptions import ObjectDoesNotExist
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
from YouWeesh.Models.Address import Address
from YouWeesh.Models.Tags import Tags
from YouWeesh.Models.Preferences import Preferences
from mongoengine.django.auth import User
from YouWeesh.Models.UsersRelationships import UsersRelationships
from mongoengine.django.auth import User
from mongoengine.queryset.visitor import Q
from YouWeesh.Tools.app import App
#from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import ensure_csrf_cookie
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
import time
from django.core.files.base import ContentFile
from base64 import b64decode
from datetime import datetime
import json

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes((AllowAny,))
def account(request, _email):
    """
    Get Account information and requests
    :param request:
    :return:
    """
    try:
        connected_user = App.getCurrentUser(request)
        selected_user = Users.objects.get(user__email=_email.lower())
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
def get_favorite_tags(request, _email):
    '''
    Get favorite tags for a user
    :param request:
    :param _email:
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        selected_user = Users.objects.get(user__email=_email)
        lstTags = list()
        lstEvents = Events.objects(Q(creator=selected_user.id) | Q(participants__contains=connected_user.id))
        lstWeesh = Wishes.objects(creator=selected_user.id)

        

        for ev in lstEvents:
            if len(ev.tags) != 0:
                lstTags.append(ev.tags[0].title.lower())
        for we in lstWeesh:
            if len(we.tags) != 0:
                lstTags.append(we.tags[0].title.lower())

        a = dict(Counter(lstTags).most_common(4))
        print json.dumps(a)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except selected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(json.dumps(a))

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def updatebackgroundpicture(request):

    try:

        connected_user = App.getCurrentUser(request)
        pictureBase64 = request.data['picture'].encode('utf8')
        picturedata = b64decode(pictureBase64)

        connected_user.preferences.background_picture.replace(ContentFile(picturedata))
        connected_user.save()

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except connected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(True)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def updatepicture(request):

    try:

        connected_user = App.getCurrentUser(request)
        pictureBase64 = request.data['picture'].encode('utf8')
        picturedata = b64decode(pictureBase64)

        connected_user.picture.replace(ContentFile(picturedata))
        connected_user.save()

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except connected_user.DoesNotExist:
        raise Http404('User doesnt exists')
    else:
        return Response(True)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getNbrFriends(request):
    try:
        connected_user = App.getCurrentUser(request)
        # TODO : Add criteria for relationships
        nbr = len(UsersRelationships.objects(from_user=connected_user.id))
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(nbr)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getFriends(request, _email):
    try:
        users = Users.objects()
        connected_user = Users.objects.get(user__email=_email)
        lstRelationships = UsersRelationships.objects(from_user=connected_user.id)
        lstFriends = list()
        for rl in lstRelationships:
            lstFriends.append(rl.to_user)
        usersSerializer = UsersSerializer(instance=lstFriends, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(usersSerializer.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def myNextEvents(request):
    try:
        connected_user = App.getCurrentUser(request)
        #TODO : Select only objects where current user is creator or participant
        lstNextEvents = Events.objects() #user_id=connected_user.id)end_date__lte=datetime.now()) #LTE a changer an SUP
        eventssrz = EventSerializer(instance=lstNextEvents, many=True)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(eventssrz.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def weeshTimeline(request):
    '''
    Get All Weeshes for profile timeline
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        lstweesh = Wishes.objects(Q(creator=connected_user.id) | Q(weeshback__contains=connected_user.id))
        lstWishes = WishSerializer(instance=lstweesh, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(lstWishes.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def eventsTimeline(request):
    '''
    Get All Events for profile timeline
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        lstevents = Events.objects(Q(creator=connected_user.id) | Q(participants__contains=connected_user.id))
        lstev = EventSerializer(instance=lstevents, many=True)

    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(lstev.data)

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createWish(request):

    try:
        _wish_title = request.POST['weesh']
        _idLevel = request.POST['idLevel']

        selectedLevel = Level.objects.get(idLevel=_idLevel)
        connected_user = App.getCurrentUser(request)
        createdWish = connected_user.create_wish(_wish_title, selectedLevel)
        wishSerializer = WishSerializer(instance=createdWish)
    except selectedLevel.DoesNotExist:
        raise Http404('Level is not existing. Check DB')
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(wishSerializer.data)



@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createEvent(request):
    """
    View used to create a wish for a user
    :rtype: object
    :param _id_user:
    :param request:
    """
    try:
        # 2 - get wish title from form
        eventName = request.data['eventName'].encode('utf8')

        start_date = request.data['startDate'].encode('utf8')
        #end_date = datetime.datetime.strptime(request.POST['endDate'], "%Y/%m/%d %H:%M")

        nbrParticipantsMax = request.data['nbrParticipantsMax'].encode('utf8')
        location = request.data['location'].encode('utf8')
        pvOrPub = request.data['pvOrPub'].encode('utf8')
        _idLevel = request.data['idLevel'].encode('utf8')
        picture = request.data['picture'].encode('utf8')

        picturedata = b64decode(picture)
        oneFile = ContentFile(picturedata)
        selectedLevel = Level.objects.get(idLevel=_idLevel)
        addr= Address()
        addr.city = location
        addr.getorUpdateCoordinates()
        addr.save()

        if request.FILES:
            thumbnail = request.FILES['thumbnail']
            App.getCurrentUser(request).create_event(eventName=eventName, start_date=start_date, thumbnail=thumbnail)
        else:
            App.getCurrentUser(request).create_event(level=selectedLevel, eventName=eventName, start_date=start_date, end_date=datetime.now(), nbrParticipantsMax=nbrParticipantsMax, address=addr, thumbnail=oneFile)

    except Users.DoesNotExist:
        raise Http404('User id does not exist')
    else:
        return Response()


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
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def useriscreated(request, email):

    try:
        users = Users.objects.get(user__email=email.lower())
        return Response(True)
    except Exception:
        return Response(False)


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
            AllWishes = Wishes.objects(Q(title__icontains=connected_user.preferences.search_string))
        if connected_user.preferences.selected_network == "FRIENDS":
            for relationship in getFriends(connected_user):
                for wish in Wishes.objects(Q(creator=relationship.from_user.id) & Q(title__icontains=connected_user.preferences.search_string)):
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
    if connected_user.preferences.display_events:
        AllEvents = list()
        if connected_user.preferences.selected_network == "PUBLIC":
            AllEvents = Events.objects(Q(title__icontains=connected_user.preferences.search_string))
        if connected_user.preferences.selected_network == "friends":
            for relationship in getFriends(connected_user):
                for wish in Events.objects(Q(creator=relationship.from_user.id) & Q(title__icontains=connected_user.preferences.search_string)):
                    AllEvents.append(wish)

        lstEvents = EventSerializer(instance=AllEvents, many=True)
        return Response(lstEvents.data)
    else:
        return None

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

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def unweeshback(request):
    '''
    Unsubscribe a the connected user to a weeshback
    :param request:
    :param _wish_id:
    :return:
    '''
    try:
        connected_user = App.getCurrentUser(request)
        current_wish = Wishes.objects.get(id=request.POST['weesh_id'])
        #Atomic update : allow not to have duplicate !
        current_wish.update(pull__weeshback=connected_user)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    except current_wish.DoesNotExist:
        raise Http404('Weesh does not exist')
    return Response(True)


@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def filter_list(request):
    """
    Define filter for the current user and record it on its preferences
    :param request:
    :return:
    """
    # 1 - record new conf into user preferences

    connected_user = App.getCurrentUser(request)
    try:
        if "eventOk" in request.POST:
            connected_user.preferences.display_events = True
        else:
            connected_user.preferences.display_events = False
        if "weeshOk" in request.POST:
            connected_user.preferences.display_weeshes = True
        else:
            connected_user.preferences.display_weeshes = False

        if "searchedString" in request.POST:
            connected_user.preferences.search_string = request.POST['searchedString']

        connected_user.preferences.selected_network = request.POST['selected_network']
        connected_user.save()
    except Wishes.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return Response(True)