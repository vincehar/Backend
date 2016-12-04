import datetime
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
from bson import ObjectId


class Wishes(Document):
    user_id = ReferenceField('Users')
    title = StringField(required=True)
    creation_date = DateTimeField(default=datetime.datetime.now())
    interested = ListField(ReferenceField('Users'))
    is_active = BooleanField(default=True)
    tags = ListField(ReferenceField('Tags'))

    def user_name(self):
        return self.user_id.username

    def get_ref_date(self):
        return self.creation_date

    def add_interested(self, user):
        self.interested.append(user)

