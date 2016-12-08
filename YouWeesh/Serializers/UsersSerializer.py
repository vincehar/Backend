from YouWeesh.Models.Users import Users
from YouWeesh.Serializers.UserSerializer import BaseUserSerializer
from YouWeesh.Serializers.PreferencesSerializer import PreferencesSerializer
from YouWeesh.Serializers.CoordinatesSerializer import CoordinatesSerializer
from rest_framework_mongoengine.serializers import DocumentSerializer


class UsersSerializer(DocumentSerializer):
    user = BaseUserSerializer()
    preferences = PreferencesSerializer()
    current_coordinates = CoordinatesSerializer()
    class Meta:
        model = Users
        depth = 1
        fields = '__all__'