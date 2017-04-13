from mongoengine import *

from YouWeesh.Models.Notifications import Notifications


class WeeshMatchingNotifications(Notifications):
    notif_type = StringField(default='WEESH_MATCHING')
    referenced_object = ReferenceField('Wishes')
    picture = ImageField()

    def referenced_object_message(self):
        return 'See profile'

    def str_notif_type(self):
        return self.notif_type
