#from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Models.SocialNetworks import SocialNetworks
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Token import Token
from YouWeesh.Tools.app import App
from mongoengine.django.auth import User


@api_view(('GET',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def loginUser(request):
    from mongoengine.queryset import DoesNotExist
    """
    si on recupere un POST, on essaie de connecter le user
    """

    ''''
    tokenCode = request.META['HTTP_AUTHORIZATION']
    tokenCode = tokenCode[8:-1]

    token = Token.objects.get(token=tokenCode)

    if token:
        user = User.objects.get(id=token.user.id)
        users = Users.objects.get(user__username=user.username)
        usersSerializer = UsersSerializer(instance=users)
        return Response(usersSerializer.data)
    else:
        return HttpResponseForbidden
    '''''
    user = App.getCurrentUser(request)
    if user is not None:
        usersSerializer = UsersSerializer(instance=user)
        return Response(usersSerializer.data)
    else:
        return HttpResponseForbidden

@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def getToken(request):
    from mongoengine.queryset import DoesNotExist
    """
    si on recupere un POST, on essaie de connecter le user
    """
    if request.method == 'POST':
        email = request.POST['username'].lower();
        password = request.POST['password']

        user = User.objects.get(email=email)
        users = Users.objects.get(user__email=email)
        socialnetworkObject = users.social_network

        if socialnetworkObject.label == 'Youweesh':
            if user.is_active and user.check_password(password):
                token = Token()
                Token.objects(user=user).update_one(user=user,token=token.generate_key(),upsert=True)

                return Response(token.get_token())
            else:
                return HttpResponseForbidden

        elif socialnetworkObject.label == 'Facebook' or socialnetworkObject.label == 'Twitter':
            token = Token()
            Token.objects(user=user).update_one(user=user,token=token.generate_key(),upsert=True)
            return Response(token.get_token())


