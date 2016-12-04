import datetime
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
import base64


class Events(Document):
    user_id = ReferenceField('Users')
    interested = ListField(ReferenceField('Users'))
    name = StringField(required=True)
    thumbnail = ImageField()
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    address = EmbeddedDocumentField('Address')
    creation_date = DateTimeField(default=datetime.datetime.now())
    price = FloatField()
    categories = ListField(EmbeddedDocumentField('Categories'))
    eventStatus = EmbeddedDocumentField('EventStatus')
    tags = ListField(ReferenceField('Tags'))
    is_active = BooleanField(default=True)
    coordinates = EmbeddedDocumentField('Coordinates')

    def get_ref_date(self):
        return self.creation_date

    def get_picture(self):
        thumbnail = base64.b64encode(self.thumbnail.read())
        return thumbnail