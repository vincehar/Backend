from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField

class Logs(Document):
    user_id = ReferenceField('Users')
    ip_address = StringField(required=True)
    date = DateTimeField(required=True)
    action = StringField(required=True)