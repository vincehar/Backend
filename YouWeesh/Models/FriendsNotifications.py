from mongoengine import *

from YouWeesh.Models.Notifications import Notifications


class FriendsNotifications(Notifications):
    notif_type = StringField(default='FRIENDS')
    referenced_object = ReferenceField('Users')
    picture = ImageField()

    def referenced_object_message(self):
        return 'See profile'

    def str_notif_type(self):
        return self.notif_type
