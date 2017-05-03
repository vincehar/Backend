from django.conf import settings
from mongoengine import *
from pyfcm import FCMNotification

from YouWeesh.Models.Notifications import Notifications


class WeeshbackNotifications(Notifications):
    notif_type = StringField(default='WEESHBACK')
    referenced_object = ReferenceField('Wishes')

    '''
    def __init__(self):
        super(WeeshbackNotifications, self).__init__(self)
        self.is_read = False
        self.referenced_object = _referenced_object
        self.content = self.referenced_object.creator.user.username + " backed you Weesh"
    '''
    def referenced_object_message(self):
        return self.referenced_object.title

    def str_notif_type(self):
        return self.notif_type

    def get_content(self):
        return self.content

    def save(self):
        super(WeeshbackNotifications, self).save()
        push_service = FCMNotification(api_key=getattr(settings, "FCM_API_KEY", None))
        registration_id = self.referenced_object.creator.fcm_token
        message_title = "Someone backed your weesh"
        message_body = self.referenced_object.title
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return result
