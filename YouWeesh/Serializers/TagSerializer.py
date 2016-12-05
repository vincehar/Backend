from YouWeesh.Models.Tags import Tags
from rest_framework_mongoengine.serializers import DocumentSerializer

from mongoengine.django.auth import User


class TagSerializer(DocumentSerializer):
   class Meta:
        model = Tags
        depth = 1
        fields = '__all__'