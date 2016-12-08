from YouWeesh.Models.Preferences import Preferences
from rest_framework_mongoengine.serializers import DocumentSerializer


class PreferencesSerializer(DocumentSerializer):
    class Meta:
        model = Preferences
        depth = 1
        fields = '__all__'