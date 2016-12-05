from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Models.UsersRelationships import UsersRelationships
from rest_framework_mongoengine.serializers import DocumentSerializer


class UsersRelationShipsSerializer(DocumentSerializer):
    from_user = UsersSerializer()
    to_user = UsersSerializer()
    class Meta:
        model = UsersRelationships
        depth = 1
        fields = '__all__'