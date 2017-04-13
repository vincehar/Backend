from mongoengine import *

from YouWeesh.Models.Notifications import Notifications


class EventsMatchingNotifications(Notifications):
    notif_type = StringField(default='EVENT_MATCHING')
    referenced_object = ReferenceField('Events')
    picture = ImageField()

    def referenced_object_message(self):
        return 'See profile'

    def str_notif_type(self):
        return self.notif_type
