from regme.views import RegisterView


class UsersBackend(RegisterView):

    def register(self, request, **kwargs):
        from upto.models import Users
        user = super(UsersBackend, self).register(request, **kwargs)
        user.save()
        profile = Users.objects.create(user=user)
        profile.save()


    def get_form_class(self):
        from upto.forms import UsersRegistrationForm
        return UsersRegistrationForm