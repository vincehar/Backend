from django.db import models as orimodels
#from mongo_auth.contrib.models import User
from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine.django.auth import User

import mongoengine

class Users(mongoengine.Document):
	user = EmbeddedModelField('User', required=True)
	wishes = ListField(EmbeddedModelField('Wishes'))

class Wishes(mongoengine.Document):
	title = mongoengine.StringField(required=True)

class EventLogUsers(mongoengine.Document):
	ip_address = mongoengine.StringField(required=True)
	connection_date = mongoengine.DateTimeField(required=True)
	users = mongoengine.ListField(EmbeddedModelField('Users'))

class Relationships(mongoengine.Document):
	users = mongoengine.ListField(EmbeddedModelField('Users'))
	users_friends = mongoengine.ListField(EmbeddedModelField('Users'))
	blocked = mongoengine.BooleanField()

class Categories(mongoengine.Document):
	name = mongoengine.StringField(required=True)

class SelectedCategories(mongoengine.Document):
	categories = mongoengine.ListField(EmbeddedModelField('Categories'))
	users = mongoengine.ListField(EmbeddedModelField('Users'))

class Messages(mongoengine.Document):
	creation_date = mongoengine.DateTimeField()
	content = mongoengine.BinaryField()
	users = mongoengine.ListField(EmbeddedModelField('Users'))
	events = mongoengine.ListField(EmbeddedModelField('Events'))

class Events(mongoengine.Document):
	name = mongoengine.StringField(required=True)
	start_date = mongoengine.DateTimeField(required=True)
	end_date = mongoengine.DateTimeField(required=True)
	address = mongoengine.StringField()
	price = mongoengine.FloatField()
	#devise = models
	categories = mongoengine.ListField(EmbeddedModelField('Categories'))
	eventStatus = mongoengine.ListField(EmbeddedModelField('EventStatus'))

class EventStatus(mongoengine.Document):
	name = mongoengine.StringField(required=True)

class Medias(mongoengine.Document):
	content = mongoengine.BinaryField()
	label = mongoengine.StringField()
	users = mongoengine.ListField(EmbeddedModelField('Users'))
	events = mongoengine.ListField(EmbeddedModelField('Events'))

class Albums(mongoengine.Document):
	events = mongoengine.ListField(EmbeddedModelField('Events'))
	name = mongoengine.StringField(required=True)