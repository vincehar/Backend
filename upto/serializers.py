from .models import Users, Wishes, Events
from rest_framework import serializers

class MySerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='abs_url', read_only=True)

    #url = serializers.URLField(source='abs_url', read_only=True) #abs_url est une function définie dans models.py
    #user = serializers.CharField(source='user_name', read_only=True) #username  est une function définie dans models.py
    #static = serializers.CharField(source='static_url', read_only=True) #static_url est une function définie dans models.py


    class Meta:
        model = Users
