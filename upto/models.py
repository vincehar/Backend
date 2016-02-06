from django.db import models as orimodels
#from mongo_auth.contrib.models import User
from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine.django.auth import User
from mongoengine import EmbeddedDocument, Document, EmbeddedDocumentField, StringField, ListField

class Wishes(EmbeddedDocument):

	title = StringField(required=True)


class Users(Document):

	user = EmbeddedDocumentField('User')
	wishes = ListField(EmbeddedDocumentField('Wishes'))
    logs = ListField(EmbeddedDocumentField('Logs'))
    friends = ListField(EmbeddedDocumentField('Relationships'))
    messages = ListField(EmbeddedDocumentField('Messages'))
    categories_Selected = ListField(EmbeddedDocumentField('Categories'))
    medias = ListField(EmbeddedDocumentField('Medias'))
    events_Owned = ListField(EmbeddedDocumentField('Events'))



class Logs(EmbeddedDocument):
    ip_address = StringField(required=True)
    date = DateTimeField(required=True)
    action = StringField(required=True)


class Relationships(EmbeddedDocument):
    friend = ListField(EmbeddedDocument('Users'))
    blocked = BooleanField()


class Categories(EmbeddedDocument):
    name = StringField(required=True)


class Messages(EmbeddedDocument):
    creation_date = DateTimeField()
    content = BinaryField()
    event = EmbeddedDocumentField('Events')


class Events(Document):
    name = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    address = StringField()
    price = FloatField()
    #devise = models
    categories = ListField(EmbeddedDocumentField('Categories'))
    eventStatus = EmbeddedDocumentField('EventStatus')


class EventStatus(EmbeddedDocument):
    name = StringField(required=True)


class Medias(Document):
    content = BinaryField()
    label = StringField()
    event = EmbeddedDocumentField('Events', required=True)
    album = EmbeddedDocumentField('Album')


class Album(EmbeddedDocument):
    name = StringField(required=True)