from rest_framework_mongoengine.serializers import DocumentSerializer
from mongoengine.django.auth import User

class BaseUserSerializer(DocumentSerializer):
   class Meta:
       model = User
       depth = 1
       fields = '__all__'
