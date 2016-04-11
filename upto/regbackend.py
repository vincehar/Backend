from regme.views import RegisterView


class UsersBackend(RegisterView):

    def register(self, request, **kwargs):
        from upto.models import Users, Preferences

        #user = super(UsersBackend, self).register(request, **kwargs)
        #user.save()
        pref = Preferences(display_events=True)
        #pref.save()
        #profile = Users.objects.create(user=user, preferences=Preferences(display_weeshes=True))
        #profile.save()


    def get_form_class(self):
        from upto.forms import UsersRegistrationForm
        return UsersRegistrationForm