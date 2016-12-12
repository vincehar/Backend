from YouWeesh.Models.Users import Users
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers


class UsersSerializer(DocumentSerializer):
    base64 = serializers.SerializerMethodField()

    class Meta:
        model = Users
        depth = 1
        fields = ('id', 'base64', 'user', 'user_id')

    def get_base64(self, users):
        return users.get_picture()