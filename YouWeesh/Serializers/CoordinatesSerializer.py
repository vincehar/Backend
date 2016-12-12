from YouWeesh.Models.Coordinates import Coordinates
from rest_framework_mongoengine.serializers import DocumentSerializer


class CoordinatesSerializer(DocumentSerializer):
    class Meta:
        model = Coordinates
        depth = 1
        fields = '__all__'