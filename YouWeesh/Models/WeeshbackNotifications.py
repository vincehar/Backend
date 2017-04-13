from mongoengine import *

from YouWeesh.Models.Notifications import Notifications


class WeeshbackNotifications(Notifications):
    notif_type = StringField(default='WEESHBACK')
    referenced_object = ReferenceField('Wishes')
    picture = ImageField()

    def referenced_object_message(self):
        return self.referenced_object.title

    def str_notif_type(self):
        return self.notif_type