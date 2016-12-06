from rest_framework_mongoengine.serializers import DocumentSerializer

from mongoengine.django.auth import User


class BaseUserSerializer(DocumentSerializer):
   class Meta:
       model = User
       fields = ('username','password')