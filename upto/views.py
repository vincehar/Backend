from django.shortcuts import render
from django.core import serializers
from django.http import Http404, HttpResponse
from mongoengine.queryset.visitor  import Q
from .models import Users, Wishes, Events, UsersRelationships
from serializers import UsersSerializer, UsersRelationShipsSerializer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import redirect
from itertools import chain
from operator import itemgetter, attrgetter, methodcaller
from collections import defaultdict
import datetime


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


@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allwishesAndEvent(request):
    if request.method == 'POST':
        request.session['username'] = request.POST['username']
    tmplst = list()
    print(request.session['username'])
    for event in Events.objects:
        tmplst.append(event)
    for wish in Wishes.objects:
        tmplst.append(wish)
    context = {
        'eventsList': sorted(tmplst, key=methodcaller('get_ref_date'), reverse=True),
        'username': request.session['username'],
    }

    #if request.accepted_renderer.format == 'html':
    return render(request, 'upto/wishes.html', context)
    #else:
    #    serializer = MySerializer(instance=context)
     #   data = serializer.data
      #  return Response(data)

def getEventInfo(request, _event_id):
    event = Events.objects.get(id=_event_id)
    current_user = Users.objects.get(user__username=request.session['username'])
    print _event_id
    context = {
        'currentEvent': event,
        'current_user': current_user,
    }

    return render(request, './upto/eventDetails.html', context)

def createWish(request):
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

    return redirect('../../upto/wishes/')

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
        return redirect('../../upto/wishes/')

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
        return redirect('../../upto/wishes/')

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
        return redirect('../../upto/wishes/')