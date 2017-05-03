from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

from YouWeesh.Models.Notifications import Notifications
from YouWeesh.Serializers.UsersSerializer import UsersSerializer


class NotificationsSerializer(DocumentSerializer):
    referenced_object_message = serializers.SerializerMethodField()
    notif_type = serializers.SerializerMethodField()
    from_user = UsersSerializer()
    to_user = UsersSerializer()

    class Meta:
        model = Notifications
        depth = 3
        fields = ('id', 'from_user', 'to_user', 'creation_date', 'is_read', 'content', 'referenced_object_message', 'notif_type')

    def get_referenced_object_message(self, FriendsNotifications):
        return FriendsNotifications.referenced_object_message()

    def get_notif_type(self, FriendsNotifications):
        return FriendsNotifications.str_notif_type()