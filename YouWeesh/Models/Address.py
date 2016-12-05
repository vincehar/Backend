from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField


class Address(EmbeddedDocument):
    address_1 = StringField()
    address_2 = StringField()
    city = StringField()
    state = StringField()
    zip_code = StringField()