from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField


class Messages(Document):
    from_user = ReferenceField('Users')
    to_user = ReferenceField('Users')
    creation_date = DateTimeField()
    content = BinaryField()
    event = EmbeddedDocumentField('Events')