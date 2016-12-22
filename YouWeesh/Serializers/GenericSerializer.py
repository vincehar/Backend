from YouWeesh.Models.Users import Users
from rest_framework_mongoengine.serializers import DocumentSerializer
from YouWeesh.Serializers.WishSerializer import WishSerializer
from YouWeesh.Serializers.EventSerializer import EventSerializer
from rest_framework import serializers


class GenericSerializer(DocumentSerializer):
    events = EventSerializer(allow_null=True)
    wishes = WishSerializer(allow_null=True)

    class Meta:
        model = None
        fields = ('wishes')