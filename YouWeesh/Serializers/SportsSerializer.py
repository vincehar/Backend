from YouWeesh.Models.Sports import Sports
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer


class SportsSerializer(DocumentSerializer):

    class Meta:
        model = Sports
        depth = 1
        fields = '__all__'
