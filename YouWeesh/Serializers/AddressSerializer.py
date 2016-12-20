from YouWeesh.Models.Address import Address
from rest_framework_mongoengine.serializers import DocumentSerializer


class AddressSerializer(DocumentSerializer):
    class Meta:
        model = Address
        depth = 1
        fields = '__all__'