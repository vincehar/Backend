from .models import Users, Wishes, Events, UsersRelationships
from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework_mongoengine.serializers import DocumentSerializer

from mongoengine.django.auth import User

class BaseUserSerializer(DocumentSerializer):
   class Meta:
       model = User
       fields = ('username','password')

class UsersSerializer(DocumentSerializer):
    class Meta:
        model = Users
        depth = 1

class UsersRelationShipsSerializer(DocumentSerializer):
    from_user = UsersSerializer()
    to_user = UsersSerializer()
    class Meta:
        model = UsersRelationships
        depth = 1