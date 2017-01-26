from YouWeesh.Models.Level import Level
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer


class LevelSerializer(DocumentSerializer):

    class Meta:
        model = Level
        depth = 1
        fields = '__all__'
