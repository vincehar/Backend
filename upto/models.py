from django.db import models as orimodels
#from mongo_auth.contrib.models import User
from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine.django.auth import User

import mongoengine


class Users(mongoengine.Document):
    user = EmbeddedModelField('User', required=True)
    wishes = ListField(EmbeddedModelField('Wishes'))
    logs = ListField(EmbeddedModelField('Logs'))
    friends = ListField(EmbeddedModelField('Relationships'))
    messages = ListField(EmbeddedModelField('Messages'))
    categories_Selected = ListField(EmbeddedModelField('Categories'))
    medias = ListField(EmbeddedModelField('Medias'))
    events_Owned = ListField(EmbeddedModelField('Events'))


class Wishes(mongoengine.Document):
    title = mongoengine.StringField(required=True)


class Logs(mongoengine.Document):
    ip_address = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)
    action = mongoengine.StringField(required=True)


class Relationships(mongoengine.Document):
    friend = mongoengine.ListField(EmbeddedModelField('Users'))
    blocked = mongoengine.BooleanField()


class Categories(mongoengine.Document):
    name = mongoengine.StringField(required=True)


class Messages(mongoengine.Document):
    creation_date = mongoengine.DateTimeField()
    content = mongoengine.BinaryField()
    event = EmbeddedModelField('Events')


class Events(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    start_date = mongoengine.DateTimeField(required=True)
    end_date = mongoengine.DateTimeField(required=True)
    address = mongoengine.StringField()
    price = mongoengine.FloatField()
    #devise = models
    categories = mongoengine.ListField(EmbeddedModelField('Categories'))
    eventStatus = EmbeddedModelField('EventStatus')


class EventStatus(mongoengine.Document):
    name = mongoengine.StringField(required=True)


class Medias(mongoengine.Document):
    content = mongoengine.BinaryField()
    label = mongoengine.StringField()
    event = EmbeddedModelField('Events', required=True)
    album = EmbeddedModelField('Album')


class Album(mongoengine.Document):
    name = mongoengine.StringField(required=True)