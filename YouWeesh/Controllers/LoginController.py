#from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
import oauth2
from YouWeesh.Models.SocialNetworks import SocialNetworks
from YouWeesh.Models.Users import Users
from YouWeesh.Models.Token import Token
from YouWeesh.Tools.app import App
from mongoengine.django.auth import User
import requests


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
        email = request.POST['email'].lower();
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


@api_view(('POST',))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def getTokenForSocialNetWork(request):
    from mongoengine.queryset import DoesNotExist
    """
    si on recupere un POST, on essaie de connecter le user
    """
    if request.method == 'POST':
        email = request.POST['email'].lower();
        socialtoken = request.POST['socialtoken']
        secretsocialtoken = request.POST['secretsocialtoken']

        try:
          user = User.objects.get(email=email)
          users = Users.objects.get(user__email=email)
          socialnetworkObject = users.social_network

          if socialnetworkObject.label == 'Facebook':
            '''
            url = 'https://graph.facebook.com/me'
            params = {'access_token': socialtoken}
            r = requests.get(url, params=params)
            userjson = r.json()
            userid = {'id':userjson['id']}
            '''
            url = 'https://graph.facebook.com/oauth/access_token'
            params = {'grant_type':'fb_exchange_token','client_id':'222535738090638','client_secret':'09a2f8b2122cd05061e50fa00dcc999a', 'fb_exchange_token':socialtoken}
            r = requests.get(url, params=params)
            longLiveSocialToken = r.content[13:]
            Token.objects(user=user).update_one(user=user,token=longLiveSocialToken,upsert=True)
            return Response(longLiveSocialToken)

          elif socialnetworkObject.label == 'Twitter':
            consumer = oauth2.Consumer(key='C7VkdO6gbb5l3xSCOXFQRX3z8', secret='CM6A2THzp1oLyqGPfFwLOcHdMVW3TS5vITdBMXOQun522bP09f')
            token = oauth2.Token(key=socialtoken, secret=secretsocialtoken)
            client = oauth2.Client(consumer, token)
            resp, content = client.request('https://api.twitter.com/1.1/account/verify_credentials.json',"GET")
            if resp['status'] == '200':
                Token.objects(user=user).update_one(user=user,token=socialtoken,upsert=True)
                return Response(socialtoken)
            else:
                return Response

            return RHttpResponseForbidden

        except Exception:

         return HttpResponseForbidden



