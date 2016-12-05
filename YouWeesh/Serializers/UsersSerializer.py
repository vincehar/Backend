from YouWeesh.Models.Users import Users
from rest_framework_mongoengine.serializers import DocumentSerializer

class UsersSerializer(DocumentSerializer):
    class Meta:
        model = Users
        depth = 1
        fields = '__all__'