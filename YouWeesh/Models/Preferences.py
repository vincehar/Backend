from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField


class Preferences(EmbeddedDocument):
    display_weeshes = BooleanField(default=True)
    display_events = BooleanField(default=True)
    search_distance = IntField(default=50)
    selected_network = StringField(default='PUBLIC')
