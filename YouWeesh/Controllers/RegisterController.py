from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Preferences import Preferences
from YouWeesh.Models.Coordinates import Coordinates
from YouWeesh.Models.SocialNetworks import SocialNetworks
from base64 import b64decode
from django.core.files.base import ContentFile
from YouWeesh.Models.Token import Token
from YouWeesh.Tools.app import App
from mongoengine.django.auth import User

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def registeruser(request):

   username = request.POST['username']
   password = request.POST['password']
   email = request.POST['email'].lower();
   lastname = request.POST['lastname']
   firstname = request.POST['firstname']
   socialnetwork = request.POST['socialnetwork']
   pictureBase64 = request.POST['picture']
   picturedata = b64decode(pictureBase64)
   socialnetworkObject = SocialNetworks.objects.get(label=socialnetwork)
   u=User.objects.create(username=username, email=email, first_name=firstname, last_name=lastname)
   if socialnetwork == 'Youweesh':
       u.set_password(password)
   u.save()
   users = Users.objects.create(user=u,social_network=socialnetworkObject,preferences=Preferences(),current_coordinates=Coordinates())
   users.picture.replace(ContentFile(picturedata))
   users.save()
   return Response(True)
