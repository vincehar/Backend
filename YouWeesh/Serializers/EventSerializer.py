from YouWeesh.Models.Events import Events
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Serializers.TagSerializer import TagSerializer
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer


class EventSerializer(DocumentSerializer):
    thumbnail = serializers.SerializerMethodField()
    creator = UsersSerializer()
    tags = TagSerializer(many=True)
    participants = UsersSerializer(many=True)
    class Meta:
        model = Events
        depth = 1
        fields = ('id', 'thumbnail', 'title', 'start_date', 'creator', 'tags', 'participants') #'start_date', 'end_date', 'price', 'name', 'user_id')

    def get_thumbnail(self, events):
        return events.get_thumbnail()