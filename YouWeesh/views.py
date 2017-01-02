import datetime
from operator import methodcaller
from django.contrib.auth import authenticate, logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from mongoengine.queryset.visitor import Q
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Serializers.EventSerializer import EventSerializer
from YouWeesh.Serializers.TagSerializer import TagSerializer
from YouWeesh.Serializers.WishSerializer import WishSerializer
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
from YouWeesh.Serializers.EventSerializer import EventSerializer
from YouWeesh.Serializers.UsersRelationShipsSerializer import UsersRelationShipsSerializer
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Wishes import Wishes
from YouWeesh.Models.Events import Events
from YouWeesh.Models.UsersRelationships import UsersRelationships
from YouWeesh.Models.Tags import Tags
from YouWeesh.Tools.app import App
from mongoengine.django.auth import User
from upto.forms import UsersLoginForm, FilterForm
from django.views.decorators.csrf import ensure_csrf_cookie
from mongoengine.queryset import DoesNotExist
#from upto.geolocalisation import geolocalisation

def index(request):
    return render(request, 'upto/index.html')

@ensure_csrf_cookie
@api_view(('GET', 'POST'))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    from mongoengine.queryset import DoesNotExist
    """
    si on recupere un POST, on essaie de connecter le user
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if request.accepted_renderer.format == 'html':
            form = UsersLoginForm(request, data=request.POST)
            try:
                if form.is_valid():
                    # user = User.objects.get(username=username)
                    user = authenticate(username=username, password=password)
                    if user.is_active and user.check_password(password):
                        user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                        request.session.set_expiry(60 * 60 * 1)
                        request.session['username'] = user.username
                        return HttpResponseRedirect('/upto/wishes/')
                else:
                    return render(request, 'upto/index.html', {'form': form})
            except DoesNotExist:
                return HttpResponseRedirect('/upto/account/register/')
                # return HttpResponse(json.dumps({'user':'not exists'}))

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
        return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        form = UsersLoginForm()
        return render(request, 'upto/index.html', {'form': form})

def logout_view(request):
    logout(request)
    form = UsersLoginForm()
    return render(request, 'upto/index.html', {'form': form})


def myevents(request):
    try:
        events_matched = list()
        connected_user = App.getCurrentUser(request)
        # - 1 get Events matching with Myweesh
        for weesh in Wishes.objects(user_id=connected_user.id, is_active=True):
            for event in Events.objects(is_active=True, tags__in=weesh.tags):
                events_matched.append(event)

        # - 2 get created events by current user
        for event in Events.objects(is_active=True, user_id=connected_user.id):
            events_matched.append(event)

        context = {
            'user': connected_user,
            'events_matched': sorted(events_matched, key=methodcaller('get_ref_date'), reverse=True)
        }
    except DoesNotExist:
        form = UsersLoginForm()
        return render(request, 'upto/index.html', {'form': form})
    else:
        # - 3 reset notifications
        return render(request, 'upto/myevents.html', context)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def userdetails(request, username):
    try:
        connected_user = App.getCurrentUser(request)
        user = Users.objects.get(user__username=username)
        context = {
                'user': user,
                'is_a_friend':False,
                'current_user': connected_user,
            }
        relations = UsersRelationships.objects.get(from_user=connected_user.id, to_user=user.id)
        if isinstance(relations, UsersRelationships):
            context = {
                'user': user,
                'is_a_friend':True,
                'current_user': connected_user,
                'relations': relations,
            }
        if request.accepted_renderer.format == 'html':
            return render(request, 'upto/userdetails.html', context)
        userSerializer = UsersSerializer(instance=user)
        return Response(userSerializer.data)
    except UsersRelationships.DoesNotExist:
        return render(request, 'upto/userdetails.html', context)


def uploadPictureUser(request):
    """
    View used to upload picture for a user
    :rtype: object
    :param _id_user:
    :param request:
    """
    try:
        connected_user = App.getCurrentUser(request)
        picture = request.FILES['picture']
        connected_user.picture.replace(picture)
        connected_user.save()

    except Users.DoesNotExist:
        raise Http404('Event id does not exist')
    else:
        return redirect('/upto/userdetails/' + connected_user.user.username)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def relationships(request, username):
    user = Users.objects.get(user__username=username)
    relationShips = UsersRelationships.objects(Q(from_user=user) | Q(to_user=user))

    context = {
        'relationShips': relationShips
    }
    if request.accepted_renderer.format == 'html':
        return render(request, 'upto/relationships.html', context)

    relationShipsSerializer = UsersRelationShipsSerializer(instance=relationShips, many=True)

    return Response(relationShipsSerializer.data)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allwishesAndEvent(request):
    try:
        #if 'username' in request.session:

            displayEventsChecked = ''
            displayWeeshesChecked = ''
            user = Users.objects.get(user__username='marc') #request.session['username'])
            if user.preferences.display_events:
                displayEventsChecked = 'checked'
            if user.preferences.display_weeshes:
                displayWeeshesChecked = 'checked'

            frmFilter = FilterForm(initial={'display_events': displayEventsChecked, 'display_weeshes': displayWeeshesChecked, 'selected_network': user.preferences.selected_network})
            wishes_user = Wishes.objects[:5](user_id=user.id).order_by('-creation_date')
            context = {
                'current_user': user,
                'wishes_user': wishes_user
                #'form': frmFilter,
            }
        #else:
        #    form = UsersLoginForm(request)
        #    return render(request, 'upto/index.html', {'form': form})
    except Users.DoesNotExist:
        raise Http404('Not logged')
    #else:
        #if request.accepted_renderer.format == 'html':
        #    return render(request, 'upto/wishes.html', context)
        #boomhttpelse:
    serializer = WishSerializer(instance=context)
    data = serializer.data
    return Response(data)

'''
@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def weeshesevents(request):
    connected_user = App.getCurrentUser(request)
    geoloc = geolocalisation()

    ### 1 - manage private and public network ###
    AllEvents = list()
    AllWishes = list()
    if connected_user.preferences.selected_network == "public":
        AllEvents = Events.objects
        AllWishes = Wishes.objects
    if connected_user.preferences.selected_network == "friends":
        for relationship in getFriends(connected_user):
            for event in Events.objects(user_id=relationship.from_user.id):
                AllEvents.append(event)
            for wish in Wishes.objects(user_id=relationship.from_user.id):
                AllWishes.append(wish)
    ### 1                                   #######
    tmplst = list()
    if connected_user.preferences.display_events:
        for event in AllEvents:
            tmplst.append(event)
    if connected_user.preferences.display_weeshes:
        for wish in AllWishes:
            tmplst.append(wish)


    context = {
        'eventsList': sorted(tmplst, key=methodcaller('get_ref_date'), reverse=True),
    }

    return render(request, 'upto/weeshesevents.html', context)
'''

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getWeeshById(request):

    wish = Wishes.objects.get(id='57270439430356405de4007a')#request.GET['id'])

    #if request.accepted_renderer.format == 'html':
    #    context = {
    #        'object': wish
    #    }
    #    return render(request, 'upto/weesh.html', context)

    wishSerializer = WishSerializer(instance=wish)
    return Response(wishSerializer.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getEventById(request):

    event = Events.objects.get(id=request.GET['id'])

    if request.accepted_renderer.format == 'html':
        context = {
            'object': event
        }
        return render(request, 'upto/event.html', context)

    if event.thumbnail:
        picture = event.get_picture()
    else:
        picture = ''

    eventSerializer = EventSerializer(instance=event)

    return Response({'event': eventSerializer.data, 'event_picture': picture})

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def popUpEvent(request):

    event = Events.objects.get(id=request.GET['id'])

    context = {
        'object': event

    }

    return render(request, 'upto/popupevent.html', context)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def popUpWeesh(request):

    weesh = Wishes.objects.get(id=request.GET['id'])

    context = {
        'object': weesh

    }

    return render(request, 'upto/popupweesh.html', context)



@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def getAutoCompleteTags(request):

    """

    :param request:
    :return:
    """
    tags = Tags.objects(title__istartswith=request.GET['tag'])
    tagSerializer = TagSerializer(instance=tags, many=True)

    return Response({'tags': tagSerializer.data})


def getUserWithUsername(_username):
    return Users.objects.get(user__username=_username)

def getEventInfo(request, _event_id):
    event = Events.objects.get(id=_event_id)
    context = {
        'currentEvent': event,
        'current_user': App.getCurrentUser(request),
    }

    return render(request, 'upto/eventDetails.html', context)



@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createWish(request):

    # 2 - get wish title from form
    _wish_title = request.POST['weeshtitle']
    App.getCurrentUser(request).create_wish(_wish_title)
    return redirect('/upto/wishes/')


def addfriend(request, username):
    try:
        connected_user = App.getCurrentUser(request)
        friend_user = getUserWithUsername(username)
        connected_user.add_friend(friend_user)
    except connected_user.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return redirect('/upto/wishes/')

def acceptfriend(request, friend_id):
    try:
        connected_user = App.getCurrentUser(request)
        relation = UsersRelationships.objects.get(from_user=friend_id, to_user=connected_user.id)
        relation_symetrical = UsersRelationships(from_user=connected_user.id, to_user=friend_id, accepted=True)
        relation.accepted = True
        relation_symetrical.save()
        relation.save()
    except connected_user.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return redirect('/upto/wishes/')

def unfriend(request, _user_id):
    try:
        connected_user = App.getCurrentUser(request)
        relation = UsersRelationships.objects.get(from_user=connected_user.id, to_user=_user_id)
        relation_symetrical = UsersRelationships.objects.get(to_user=connected_user.id, from_user=_user_id)
        relation_symetrical.delete()
        relation.delete()
    except connected_user.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
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
        # 2 - get wish title from form
        eventName = request.POST['eventName']

        start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y/%m/%d %H:%M")
        end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y/%m/%d %H:%M")

        if request.FILES:
            thumbnail = request.FILES['thumbnail']
            App.getCurrentUser(request).create_event(eventName=eventName, start_date=start_date, end_date=end_date, thumbnail=thumbnail)
        else:
            App.getCurrentUser(request).create_event(eventName=eventName, start_date=start_date, end_date=end_date)

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


def filter_list(request):
    """
    Define filter for the current user and record it on its preferences
    :param request:
    :return:
    """
    # 1 - record new conf into user preferences
    connected_user = App.getCurrentUser(request)
    if request.method == "POST":
        try:
            if "display_events" in request.POST:
                connected_user.preferences.display_events = True
            else:
                connected_user.preferences.display_events = False
            if "display_weeshes" in request.POST:
                connected_user.preferences.display_weeshes = True
            else:
                connected_user.preferences.display_weeshes = False
            connected_user.preferences.selected_network = request.POST['selected_network']
            connected_user.save()
        except Wishes.DoesNotExist:
            raise Http404('Wish id does not exist')
        else:
            return redirect('/upto/wishes/')

def weeshback(request, _wish_id):
    connected_user = App.getCurrentUser(request)
    weesh = Wishes.objects.get(id=_wish_id)
    weesh.add_interested(connected_user)
'''
def geoloc(request):
    from geolocalisation import geolocalisation
    geo = geolocalisation()

    matrix = geo.getDistance()
    for row in matrix['rows']:
        for element in row['elements']:
             distance = element['distance']['text']

    #return distance
    return render(request, 'upto/testGeoLocalisation.html')


def getDistanceTextFormat(request, origin, destination):
    from geolocalisation import geolocalisation
    geo = geolocalisation()

    matrix = geo.getDistance(origin, destination)
    for row in matrix['rows']:
        for element in row['elements']:
             distance = element['distance']['text']

    return distance
    #return render(request, 'upto/testGeoLocalisation.html')
'''

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def saveCurrentPosition(request):
    """
    Define the current position of the current user
    :param request:
    """
    connected_user = Users.objects.get(user__username='marc')
    #'Tools.getCurrentUser(request)
    lat = request.GET['lat']
    lng = request.GET['lng']

    connected_user.current_coordinates.lattitude = float(lat)
    connected_user.current_coordinates.longitude = float(lng)
    connected_user.save()
    return Response({'status': 0})