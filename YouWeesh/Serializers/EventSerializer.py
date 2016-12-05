from YouWeesh.Models import Users, Wishes, Events, UsersRelationships, Tags
#from rest_framework import serializers
#from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework_mongoengine.serializers import DocumentSerializer

from mongoengine.django.auth import User


class EventSerializer(DocumentSerializer):
   class Meta:
        model = Events
        depth = 1
        fields = '__all__'