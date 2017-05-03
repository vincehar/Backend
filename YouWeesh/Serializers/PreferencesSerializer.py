from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

from YouWeesh.Models.Preferences import Preferences


class PreferencesSerializer(DocumentSerializer):

    background_picture = serializers.SerializerMethodField()

    class Meta:
        model = Preferences
        depth = 1
        fields = ('display_weeshes', 'display_events', 'background_picture', 'selected_network', 'search_string')

    def get_background_picture(self, Preferences):
        return Preferences.get_background_picture()