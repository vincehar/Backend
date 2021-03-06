from YouWeesh.Models.Users import Users
from rest_framework_mongoengine.serializers import DocumentSerializer
from YouWeesh.Serializers.PreferencesSerializer import PreferencesSerializer
from YouWeesh.Serializers.AddressSerializer import AddressSerializer
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
from rest_framework import serializers


class UsersSerializer(DocumentSerializer):
    base64 = serializers.SerializerMethodField()
    preferences = PreferencesSerializer()
    address = AddressSerializer()
    user = BaseUserSerializer()

    class Meta:
        model = Users
        depth = 2
        fields = ('id', 'user', 'base64', 'user_id', 'preferences', 'current_coordinates', 'date_created', 'address')

    def get_base64(self, Users):
        return Users.get_picture()