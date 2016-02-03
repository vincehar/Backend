from django.db import models as orimodels
from mongo_auth.contrib.models import User
from djangotoolbox.fields import ListField, EmbeddedModelField
import mongoengine

class Users(mongoengine.Document):

	user = EmbeddedModelField('User')
