from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Users, Wishes, Events
from serializers import MySerializer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response



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


def userdetails(request, username):
    user = Users.objects.get(user__username=username)
    context = {
        'user': user,
    }
    return render(request, 'upto/userdetails.html', context)


def allwishesAndEvent(request):

    w = Users.objects.order_by('events_Owned.start_date').only('wishes')
    e = Users.objects.order_by('events_Owned.start_date').only('events_Owned')
    context = {
        'user_wishes': w,
        'user_events': e,
    }
    if request.accepted_renderer.format == 'html':

    return render(request, 'upto/wishes.html', context)

@api_view(('GET',))
@permission_classes((IsAuthenticated, ))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def viewprofile(request, userid):
        if request.user.is_authenticated():
                pro = Profile.objects.get(user_id=userid)
                if request.accepted_renderer.format == 'html':
                        data = {'profile' : pro}
                        return Response(data, template_name='network/profile.html')
                serializer = MySerializer(instance=pro)
                data = serializer.data
                return Response(data)

@api_view(('DATA',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes((AllowAny, ))
def list_profiles(request):
        ch = request.DATA.get('chaine')
        queryset = Profile.objects.all().filter(user__username__icontains=ch)

        if request.accepted_renderer.format == 'html':
                data = {'profile' : queryset, 'request' : request}
                return Response(data, template_name='network/searchresult.html')

        serializer = MySerializer(instance=queryset, many=True)
        data = serializer.data
        return Response(data)
