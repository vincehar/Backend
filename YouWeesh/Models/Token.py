import datetime
import base64
from mongoengine.django.auth import User
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
from bson import ObjectId
import binascii
import os

class Token(Document):
    """
    Main class representing the Users entities.
    This is the class in which everything is embedded.
    """
    token = StringField()
    user = ReferenceField('User')
    date_created = DateTimeField(default=datetime.datetime.now())

    def get_token(self):
        """
        Return formatted position
        #{ "lat" : 46.1954229 , "lng" : 6.1552161 }
        :return:
        """
        return self.token

    def generate_key(self):
        self.token = binascii.hexlify(os.urandom(20)).decode()
        return self.token

    def get_date_created(self):
        """
        Get the date when the user has registered.
        :return: datetime.datetime
        """
        return self.date_created

