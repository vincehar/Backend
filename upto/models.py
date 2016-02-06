from django.db import models as orimodels
#from mongo_auth.contrib.models import User
#from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine.django.auth import User
from mongoengine import EmbeddedDocument, Document, EmbeddedDocumentField, StringField, ListField

class Wishes(EmbeddedDocument):

	title = StringField(required=True)


class Users(Document):

	user = EmbeddedDocumentField('User')
	wishes = ListField(EmbeddedDocumentField('Wishes'))

