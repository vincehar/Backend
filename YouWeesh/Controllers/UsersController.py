from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from YouWeesh.Serializers import UsersSerializer, EventSerializer
from YouWeesh.Models.Users import Users, Events
from mongoengine.django.auth import User
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
from YouWeesh.Models.UsersRelationships import UsersRelationships
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
from datetime import datetime

@permission_classes((IsAuthenticated,))
def account(request):
    """
    Get Account information and requests
    :param request:
    :return:
    """
    try:
        connected_user = getConnectedUser(request)
        friends_requests = UsersRelationships.objects(accepted=False, to_user=connected_user.id) #UsersRelationships.objects.get(to_user=connected_user.id)
        my_friends = UsersRelationships.objects(accepted=True, to_user=connected_user.id)

        context = {
            'user': connected_user,
            'friends_requests': friends_requests,
            'my_friends': my_friends,
        }
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return render(request, 'upto/myaccount.html', context)


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getFriends(request):
    try:
        connected_user = Users.objects.get(user__username='marc')
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
        lstNextEvents = Events.objects.get(user_id=connected_user.id, end_date__lte=datetime.now()) #LTE a changer an SUP
        events = EventSerializer(instance=lstNextEvents, many=True)
    except connected_user.DoesNotExist:
        raise Http404('Not logged')
    else:
        return Response(events.data)


@api_view(('GET','POST'))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    from mongoengine.queryset import DoesNotExist
    """
    si on recupere un POST, on essaie de connecter le user
    """
    if request.method == 'POST':
        username = request.POST['username'].lower();
        password = request.POST['password']

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





