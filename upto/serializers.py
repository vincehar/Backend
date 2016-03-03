from .models import Users, Wishes, Events
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

from mongoengine.django.auth import User


class UserDetailsSerializer(DocumentSerializer):
    class Meta:
        model = Users
        depth = 1