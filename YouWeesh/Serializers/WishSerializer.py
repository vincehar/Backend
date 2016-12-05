from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Serializers.TagSerializer import TagSerializer
from YouWeesh.Models.Wishes import Wishes
from rest_framework_mongoengine.serializers import DocumentSerializer


class WishSerializer(DocumentSerializer):
   user_id = UsersSerializer()
   tags = TagSerializer(many=True)
   class Meta:
        model = Wishes
        depth = 1
        fields = '__all__'