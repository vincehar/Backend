from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Users, Wishes, Events
from serializers import UserDetailsSerializer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
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

    if request.accepted_renderer.format == 'html':
        context = {
            'user': user,
        }
        return render(request, 'upto/userdetails.html', context)

    #no comment
    serializer = UserDetailsSerializer(instance=user)
    return Response(serializer.data)


@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allwishesAndEvent(request):
    tmplst = list()

    for event in Events.objects:
        tmplst.append(event)
    for wish in Wishes.objects:
        tmplst.append(wish)
    context = {
        'eventsList': sorted(tmplst, key=methodcaller('get_ref_date'), reverse=True),
        'users': Users.objects
    }

    #if request.accepted_renderer.format == 'html':
    return render(request, 'upto/wishes.html', context)
    #else:
    #    serializer = MySerializer(instance=context)
     #   data = serializer.data
      #  return Response(data)

def getEventInfo(request, _event_id):
    event = Events.objects.get(id=_event_id)
    context = {
        'currentEvent': event,
    }

    return render(request, 'upto/eventDetails.html', context)

def createWish(request, _user_id):
    """
    View used to create a wish for a user
    :rtype: object
    :param _id_user:
    :param request:
    """
    #1 - get user with id
    current_user = _user_id
    #2 - get wish title from form
    _wish_title = request.POST['wish']
    current_user.create_wish(_wish_title)
    return render(request, 'upto/wishes.html')

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
        print request.POST['user_id']
        current_user = Users.objects.get(id=request.POST['user_id'])
        #2 - get wish title from form
        eventName = request.POST['eventName']

        start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d %H:%M")
        end_date = datetime.datetime.strptime(request.POST['end_date'], "%Y-%m-%d %H:%M")

        current_user.create_event(eventName, start_date, end_date)
    except Users.DoesNotExist:
        raise Http404('Event id does not exist')
    else:
        return render(request, 'upto/wishes.html')