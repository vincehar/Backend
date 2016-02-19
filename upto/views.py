from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Users, Wishes, Events
#from serializers import MySerializer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from itertools import chain
from operator import itemgetter, attrgetter, methodcaller
from collections import defaultdict


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
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def user_info(request, nom_user):
    user_name = nom_user
    user = Users.objects.get(user__username=user_name)
    context = {
        'user': user,
    }
    #if request.accepted_renderer.format == 'html':
    return render(request, 'upto/accountDetails.html', context)
    #else:
    #    serializer = MySerializer(instance=context)
    #    data = serializer.data
    #    return Response(data)

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allwishesAndEvent(request):
    tmplst = list()
    usersList = Users.objects
    for user in usersList:
        for event in user.events_Owned:
                tmplst.append(event)
        for wish in user.wishes:
                tmplst.append(wish)
    context = {
        'eventsList': sorted(tmplst, key=methodcaller('get_ref_date'), reverse=True),
    }

    #if request.accepted_renderer.format == 'html':
    return render(request, 'upto/wishes.html', context)
    #else:
    #    serializer = MySerializer(instance=context)
     #   data = serializer.data
      #  return Response(data)

def getEventInfo(request, _event_id):
    context = {
        'currentEvent': Users.objects.get(events_Owned__event_id=_event_id)
    }
    return render(request, 'upto/eventDetails.html', context)

