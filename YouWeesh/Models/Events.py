import datetime
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
import base64


class Events(Document):
    creator = ReferenceField('Users')
    interested = ListField(ReferenceField('Users'))
    title = StringField(required=True)
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

    def get_thumbnail(self):
        if self.thumbnail:
            picture = base64.b64encode(self.thumbnail.read())
            return picture
        else:
            return None