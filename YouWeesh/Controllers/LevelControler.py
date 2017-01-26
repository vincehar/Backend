from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from YouWeesh.Serializers.LevelSerializer import LevelSerializer
from YouWeesh.Models.Level import Level

@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, ))
def getLevels(request):
    selectedLevel = Level.objects
    levels = LevelSerializer(instance=selectedLevel, many=True)
    return Response(levels.data)
