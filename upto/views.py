import datetime
import pickle
from operator import methodcaller
import django.core.exceptions
from django.contrib.auth import authenticate, logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from mongoengine.queryset.visitor import Q
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from serializers import UsersSerializer, UsersRelationShipsSerializer, BaseUserSerializer, WishSerializer, EventSerializer
from .models import Users, Wishes, Events, UsersRelationships, Preferences
from mongoengine.django.auth import User
from upto.forms import UsersLoginForm, FilterForm
from django.views.decorators.csrf import ensure_csrf_cookie


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


@permission_classes((IsAuthenticated,))
def account(request):
    # test with a user
    user_id = Users.objects.get(user__username=request.session['username']).id
    user = Users.objects.get(id=user_id)
    context = {
        'one_user': user,
    }
    return render(request, 'upto/myaccount.html', context)


'''
--------- A GARDER ------

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
'''


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def userdetails(request, username):
    try:
        connected_user = getConnectedUser(request)
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
        connected_user = getConnectedUser(request)
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
@permission_classes((IsAuthenticated,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allwishesAndEvent(request):
    try:
        if 'username' in request.session:
            displayEventsChecked = ''
            displayWeeshesChecked = ''
            user = Users.objects.get(user__username=request.session['username'])
            if user.preferences.display_events:
                displayEventsChecked = 'checked'
            if user.preferences.display_weeshes:
                displayWeeshesChecked = 'checked'

            frmFilter = FilterForm(initial={'display_events': displayEventsChecked, 'display_weeshes': displayWeeshesChecked})
            print frmFilter
            wishes_user = Wishes.objects[:5](user_id=user.id).order_by('-creation_date')
            context = {
                'current_user': user,
                'wishes_user': wishes_user,
                'form': frmFilter,
            }
        else:
            form = UsersLoginForm(request)
            return render(request, 'upto/index.html', {'form': form})
    except Users.DoesNotExist:
        raise Http404('Not logged')
    else:
        if request.accepted_renderer.format == 'html':
            return render(request, 'upto/wishes.html', context)
        else:
            serializer = WishSerializer(instance=context)
            data = serializer.data
            return Response(data)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def weeshesevents(request):
    connected_user = getConnectedUser(request)
    tmplst = list()
    print connected_user.preferences.display_events
    if connected_user.preferences.display_events:
        for event in Events.objects:
            tmplst.append(event)
    if connected_user.preferences.display_weeshes:
        for wish in Wishes.objects:
            tmplst.append(wish)
    context = {
        'eventsList': sorted(tmplst, key=methodcaller('get_ref_date'), reverse=True)
    }

    return render(request, 'upto/weeshesevents.html', context)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def getWeeshById(request):

    wish = Wishes.objects(wish_id=request.GET['id'])
    username = wish[0].user_id.user.username
    wishSerializer = WishSerializer(instance=wish,many=True)

    return Response({'wish': wishSerializer.data, 'username': username})

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def getEventById(request):

    event = Events.objects(event_id=request.GET['id'])
    username = event[0].user_id.user.username
    picture = event[0].get_picture()
    eventSerializer = EventSerializer(instance=event,many=True)

    return Response({'event': eventSerializer.data, 'event_picture': picture, 'username': username})


def getConnectedUser(request):
    return Users.objects.get(user__username=request.session['username'])

def getUserWithUsername(_username):
    return Users.objects.get(user__username=_username)

def getEventInfo(request, _event_id):
    event = Events.objects.get(id=_event_id)
    print _event_id
    context = {
        'currentEvent': event,
        'current_user': getConnectedUser(request),
    }

    return render(request, 'upto/eventDetails.html', context)


@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def createWish(request):
    """
    View used to create a wish for a user
    :rtype: object
    :param _id_user:
    :param request:
    """
    # 2 - get wish title from form
    _wish_title = request.POST['weeshtitle']
    getConnectedUser(request).create_wish(_wish_title)
    return redirect('/upto/wishes/')

def addfriend(request, username):
    try:
        connected_user = getConnectedUser(request)
        friend_user = getUserWithUsername(username)
        connected_user.add_friend(friend_user)
    except connected_user.DoesNotExist:
        raise Http404('Wish id does not exist')
    else:
        return redirect('/upto/wishes/')

def unfriend(request, _user_id):
    try:
        connected_user = getConnectedUser(request)
        relation = UsersRelationships.objects.get(from_user=connected_user.id, to_user=_user_id)
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
        thumbnail = request.FILES['thumbnail']

        getConnectedUser(request).create_event(eventName, start_date, end_date, thumbnail)
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

    :param request:
    :return:
    """
    # 1 - record new conf into user preferences
    connected_user = getConnectedUser(request)
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
            # 2 - call view weeshesAndEvents with filter
            connected_user.save()
        except Wishes.DoesNotExist:
            raise Http404('Wish id does not exist')
        else:
            return redirect('/upto/wishes/')
