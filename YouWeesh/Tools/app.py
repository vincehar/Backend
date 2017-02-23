from YouWeesh.Models.Users import Users
from YouWeesh.Models.Token import Token
from mongoengine.django.auth import User

class App(object):

    @staticmethod
    def getCurrentUser(request):
        try:
            tokenCode = request.META['HTTP_AUTHORIZATION']
            tokenCode = tokenCode[7:]

            token = Token.objects.get(token=tokenCode)

            if token:
                user = User.objects.get(id=token.user.id)
                users = Users.objects.get(user__email=user.email)
                return users
            else:
                return None

        except Exception:
            return None
