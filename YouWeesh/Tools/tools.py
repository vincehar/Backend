from YouWeesh.Models.Users import Users
from YouWeesh.Models.Token import Token
from mongoengine.django.auth import User

class Tools(object):

    @staticmethod
    def getCurrentUser(request):
        try:
            tokenCode = request.META['HTTP_AUTHORIZATION']
            tokenCode = tokenCode[8:-1]

            token = Token.objects.get(token=tokenCode)

            if token:
                user = User.objects.get(id=token.user.id)
                users = Users.objects.get(user__username=user.username)
                return users
            else:
                return None

        except Exception:
            return None
