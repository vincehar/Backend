from django.conf import settings
from mongoengine import *
from pyfcm import FCMNotification

from YouWeesh.Models.Notifications import Notifications


class FriendsNotifications(Notifications):
    notif_type = StringField(default='FRIENDS')
    referenced_object = ReferenceField('Users')

    def referenced_object_message(self):
        return 'See profile of ' + self.referenced_object.user.username

    def str_notif_type(self):
        return self.notif_type

    def save(self):
        super(FriendsNotifications, self).save()
        push_service = FCMNotification(api_key=getattr(settings, "FCM_API_KEY", None))
        registration_id = self.referenced_object.fcm_token
        message_title = self.content
        message_body = message_title
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return result
