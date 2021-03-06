import datetime

from mongoengine import Document, ReferenceField, StringField, ListField, DateTimeField, BooleanField


class Wishes(Document):
    creator = ReferenceField('Users')
    title = StringField(required=True)
    creation_date = DateTimeField(default=datetime.datetime.now())
    weeshback = ListField(ReferenceField('Users'))
    is_active = BooleanField(default=True)
    tags = ListField(ReferenceField('Tags'))
    level = ReferenceField('Level')

    def user_name(self):
        return self.user_id.username

    def get_ref_date(self):
        return self.creation_date

    def add_interested(self, user):
        self.weeshback.append(user)

