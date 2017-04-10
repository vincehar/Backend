from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from YouWeesh.Serializers.SportsSerializer import SportsSerializer
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Sports import Sports
from YouWeesh.Models.Preferences import Preferences
from YouWeesh.Models.Coordinates import Coordinates
from YouWeesh.Models.SocialNetworks import SocialNetworks
from base64 import b64decode
from django.core.files.base import ContentFile
from YouWeesh.Models.Token import Token
from YouWeesh.Tools.app import App
from mongoengine.django.auth import User

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, ))
def getsports(request, searchterm):
    '''
    :return:
    '''

    sports = Sports.objects(label__icontains=searchterm).only("label")
    sportsSerialized = SportsSerializer(instance=sports, many=True)

    return Response(sportsSerialized.data)

    '''
    Model.objects(refs__contains="5305c92956c02c3f391fcaba")._query
    '''