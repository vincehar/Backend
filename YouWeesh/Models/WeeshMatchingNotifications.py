from django.conf import settings
from mongoengine import *
from pyfcm import FCMNotification

from YouWeesh.Models.Notifications import Notifications


class WeeshMatchingNotifications(Notifications):
    notif_type = StringField(default='WEESH_MATCHING')
    referenced_object = ReferenceField('Wishes')

    def referenced_object_message(self):
        return self.referenced_object.title

    def str_notif_type(self):
        return self.notif_type

    def get_content(self):
        return self.content

    def save(self):
        super(WeeshMatchingNotifications, self).save()
        push_service = FCMNotification(api_key=getattr(settings, "FCM_API_KEY", None))
        registration_id = self.referenced_object.creator.fcm_token
        message_title = "One of your weeshes is matching !"
        message_body = self.referenced_object.title
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return result