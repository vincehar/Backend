import datetime
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
from bson import ObjectId


class UsersRelationships(Document):
    """
    Class used to manage relationships beetwen Users instances.
    """
    rel_id = ObjectIdField(default=ObjectId)
    from_user = ReferenceField('Users')
    to_user = ReferenceField('Users')
    accepted = BooleanField()
    blocked = BooleanField(default=False)
    date_created = DateTimeField(default=datetime.datetime.now())

    def accept(self):
        """
        Method used to make a relationship symetrical, i.e user a follows back user b.
        :return: self
        """
        self.accepted=True
        return self