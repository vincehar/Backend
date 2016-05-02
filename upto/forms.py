from django import forms
from mongodbforms import DocumentForm, EmbeddedDocumentForm
from django.contrib.auth.forms import AuthenticationForm
from regme.documents import User
from upto.models import Users, Preferences
from regme.forms import UserCreationForm
from django.forms.widgets import Input
from django.core.validators import *
from rabbitmq import rabbitmq

class RangeInput(Input):
    """HTML5 Range Input."""
    input_type = 'range'


class UsersRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2")

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def save(self):
        user = super(UsersRegistrationForm, self).save()
        profile = Users(user=user, preferences=Preferences())
        # user.is_active = False
        user.save()
        profile.save()

        print('Salut')

        #Connect and create the queue for the user
        myrabbit = rabbitmq()
        myrabbit.create_connection()
        myrabbit.create_queue(profile)
        myrabbit.close()

class UsersLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class FilterForm(forms.Form):
    #class Meta:
        #model = Preferences
        #fields = ['display_events', 'display_weeshes', 'selected_network', 'search_distance']
        display_events = forms.CharField(label='Events', max_length=100, widget=forms.CheckboxInput)
        display_weeshes = forms.CharField(label='Weeshes', max_length=100, widget=forms.CheckboxInput)
        CHOICES = [('public', 'Public'),
                   ('friends', 'Friends')]
        selected_network = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
        search_distance = forms.CharField(widget=RangeInput(), validators=[MaxValueValidator(10), MinValueValidator(1)])
#class CreateEventForm(forms.Form):
