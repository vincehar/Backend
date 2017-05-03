import datetime

from mongoengine import Document, ReferenceField, StringField, DateTimeField, BooleanField


class Notifications(Document):
    meta ={'allow_inheritance': True}
    from_user = ReferenceField('Users')
    to_user = ReferenceField('Users')
    creation_date = DateTimeField(default=datetime.datetime.now())
    is_read = BooleanField(default=False)
    content = StringField()
