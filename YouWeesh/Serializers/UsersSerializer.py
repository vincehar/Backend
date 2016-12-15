from YouWeesh.Models.Users import Users
from rest_framework_mongoengine.serializers import DocumentSerializer
from YouWeesh.Serializers.PreferencesSerializer import PreferencesSerializer
from rest_framework import serializers


class UsersSerializer(DocumentSerializer):
    base64 = serializers.SerializerMethodField()
    preferences = PreferencesSerializer()
    class Meta:
        model = Users
        depth = 1
        fields = ('id', 'base64', 'user', 'user_id', 'preferences', 'current_coordinates', 'date_created')

    def get_base64(self, users):
        return users.get_picture()