from YouWeesh.Models.Events import Events
from YouWeesh.Serializers.UsersSerializer import UsersSerializer
from YouWeesh.Serializers.TagSerializer import TagSerializer
from YouWeesh.Serializers.LevelSerializer import LevelSerializer
from YouWeesh.Serializers.AddressSerializer import AddressSerializer
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer


class EventSerializer(DocumentSerializer):
    thumbnail = serializers.SerializerMethodField()
    level = LevelSerializer()
    creator = UsersSerializer()
    tags = TagSerializer(many=True)
    participants = UsersSerializer(many=True)
    address = AddressSerializer()

    class Meta:
        model = Events
        depth = 1
        fields = ('id', 'thumbnail', 'title', 'start_date', 'creator', 'tags', 'participants', 'level', 'address', 'description', 'priv_or_pub', 'nbrParticipantsMax') #'start_date', 'end_date', 'price', 'name', 'user_id')

    def get_thumbnail(self, events):
        return events.get_thumbnail()