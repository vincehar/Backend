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
from YouWeesh.Serializers.UsersRelationShipsSerializer import UsersRelationships
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Wishes import Wishes
from YouWeesh.Models.Events import Events
from YouWeesh.Models.UsersRelationships import UsersRelationships
from YouWeesh.Models.Tags import Tags
from mongoengine.django.auth import User
from upto.forms import UsersLoginForm, FilterForm
from django.views.decorators.csrf import ensure_csrf_cookie
from mongoengine.queryset import DoesNotExist

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getWeeshById(request, _wish_id):

    wish = Wishes.objects.get(id=_wish_id)
    wishSerializer = WishSerializer(instance=wish)
    return Response(wishSerializer.data)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getWeeshBackCount(request, _wish_id):
    wish = Wishes.objects.get(id=_wish_id)
    nbrWeeshBack = len(wish.weeshback)
    return Response(nbrWeeshBack)

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def getWeeshBackUsers(request, _wish_id):
    wish = Wishes.objects.get(id=_wish_id)
    usersSerializer = UsersSerializer(wish.weeshback)
    return Response(usersSerializer.data)