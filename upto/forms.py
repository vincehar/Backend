from mongodbforms import DocumentForm
from django import forms
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
#from mongoengine.django.auth import User
from regme.documents import User
from upto.models import Users
from regme.forms import UserCreationForm



class UsersRegistrationForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username",
				  "email",
				  "password1",
				  "password2")

	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class':'form-control'}))


	def save(self):
		user = super(UsersRegistrationForm, self).save()
		profile = Users(user=user)
		user.is_active = False
		user.save()
		profile.save()

class UsersLoginForm(AuthenticationForm):
	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class':'form-control'}))