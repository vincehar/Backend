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

    serializer = UserDetailsSerializer(instance=user)
    return Response(serializer.data)


    #    serializer = MySerializer(instance=context)
    #    data = serializer.data
    #    return Response(data)

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def allwishesAndEvent(request):
    eventsList = list()
    wishesAndEvents = Users.objects

    for users in wishesAndEvents:
        #1 - lister tous les wishes + users
        for event in users.events_Owned:
            eventsList.append(event)
         #2 - lister tous les events + users
        for wish in users.wishes:
            eventsList.append(wish)

    #3 - Append list Object + users (string)
    context = {
        'wishesAndEvent': wishesAndEvents,
        'eventsList': eventsList,#sorted(eventsList, key=methodcaller('get_ref_date'), reverse=True),
    }
    #if request.accepted_renderer.format == 'html':
    return render(request, 'upto/wishes.html', context)
    #else:
    #    serializer = MySerializer(instance=context)
     #   data = serializer.data
      #  return Response(data)
