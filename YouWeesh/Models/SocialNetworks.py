from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField


class SocialNetworks(Document):
    """
    Main class representing the Users entities.
    This is the class in which everything is embedded.
    """
    label = StringField()

