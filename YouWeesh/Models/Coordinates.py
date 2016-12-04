import datetime
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField


class Coordinates(EmbeddedDocument):
    lat = FloatField(default=5)
    lng = FloatField(default=5)
    update_date = DateTimeField(default=datetime.datetime.now())