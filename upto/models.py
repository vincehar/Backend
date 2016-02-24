from django.core.mail.backends.console import EmailBackend
from django.db import models as orimodels
#from mongo_auth.contrib.models import User
from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine.django.auth import User
import datetime
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField
from bson import ObjectId


class Wishes(EmbeddedDocument):
    user_id = ReferenceField('Users')
    wish_id = ObjectIdField(default=ObjectId)
    title = StringField(required=True)
    creation_date = DateTimeField()
    interested = ListField(ReferenceField('Users'))

    def get_ref_date(self):
	return self.creation_date

def add_interested(self, user):
    self.interested.append(user)


class Logs(EmbeddedDocument):
    ip_address = StringField(required=True)
    date = DateTimeField(required=True)
    action = StringField(required=True)


class Categories(EmbeddedDocument):
    name = StringField(required=True)


class Messages(EmbeddedDocument):
    creation_date = DateTimeField()
    content = BinaryField()
    event = EmbeddedDocumentField('Events')

class EventStatus(EmbeddedDocument):
    name = StringField(required=True)

class Address(EmbeddedDocument):
    address_1 = StringField()
    address_2 = StringField()
    city = StringField()
    state = StringField()
    zip_code = StringField()

class Events(Document):
    user_id = ReferenceField('Users')
    event_id = ObjectIdField(default=ObjectId)
    name = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    address = EmbeddedDocumentField('Address')
    price = FloatField()
    #devise = models
    categories = ListField(EmbeddedDocumentField('Categories'))
    eventStatus = EmbeddedDocumentField('EventStatus')

    def get_ref_date(self):
        return self.start_date


class Album(EmbeddedDocument):
    name = StringField(required=True)

class Medias(Document):
    content = BinaryField()
    label = StringField()
    event = EmbeddedDocumentField('Events', required=True)
    album = EmbeddedDocumentField('Album')

class UsersRelationships(EmbeddedDocument):
    """
    Class used to manage relationships beetwen Users instances.
    """
    RELATIONSHIPS_TYPES = (
        ('Follower', 'Follower'),
        ('Followed', 'Followed'),
    )

    rel_id = ObjectIdField(default=ObjectId)
    from_user = ReferenceField('Users')
    to_user = ReferenceField('Users')
    active = BooleanField()
    symetrical = BooleanField()
    blocked = BooleanField()
    status = StringField(choices=RELATIONSHIPS_TYPES)
    date_created = DateTimeField(default=datetime.datetime.now())

    def make_symetrical(self):
        """
        Method used to make a relationship symetrical, i.e user a follows back user b.
        :return: self
        """
        self.active=True
        self.symetrical=True
        return self

    def activate(self):
        self.active=True
        return self


class Users(Document):
    """
    Main class representing the Users entities.
    This is the class in which everything is embedded.
    """
    user_id = ObjectIdField(default=ObjectId)
    user = EmbeddedDocumentField('User')
    wishes = ListField(EmbeddedDocumentField('Wishes'))
    logs = ListField(EmbeddedDocumentField('Logs'))
    friends = ListField(EmbeddedDocumentField('UsersRelationships'))
    messages = ListField(EmbeddedDocumentField('Messages'))
    categories_Selected = ListField(EmbeddedDocumentField('Categories'))
    medias = ListField(EmbeddedDocumentField('Medias'))
    events_Owned = ListField(EmbeddedDocumentField('Events'))
    interested_in = ListField(EmbeddedDocumentField('Wishes'))

    def date_joined(self):
        """
        Get the date when the user has registered.
        :return: datetime.datetime
        """
        return self.user.date_joined

    def relate_to_user(self, user):
        """
        Method used to relate to another user, i.e follow a user.
        :param user: instance of Users class
        :return: self
        """
        rel = UsersRelationships(from_user=self, to_user=None, active=False, symetrical=False, blocked=False, status='Follower')
        user.friends.append(rel)
        relself = UsersRelationships(from_user=None, to_user=user, active=False, symetrical=False, blocked=False, status='Followed')
        self.friends.append(relself)
        user.save()
        self.save()
        return self

    def make_symerical_relationship(self, user):
        """
        Method used to follow a user that already follows you, i.e follow back a user.
        :param user: instance of Users class
        :return: self
        """
        Users.objects(friends__from_user=user, friends__to_user=self).update(set__friends__S__active=True, set__friends__S__symetrical=True)
        self.save()
        return self

    def accept_follower(self, user):
        """
        Method used to activate a relationship, i.e accept a follower
        :param user:
        :return:
        """
        Users.objects(friends__from_user=user, friends__to_user=self).update(set__friends__S__active=True)
        self.save()
        return self

    def create_wish(self, _title, _creation_date):
        """
        Method used to create a wish
        :param _title:
        :param _creation_date:
        :return: self
        """
        wish = Wishes(user_id=self.id, title=_title, creation_date=_creation_date)
        self.wishes.append(wish)
        wish.save()
        self.save()
        return self


    def create_event(self, _name, _start_date, _end_date):
        """
        Method user to create an event
        :param _user:
        :param _name:
        :param _startDate:
        :param _endDate:
        :return: self
        """
        event = Events(user_id=self.id, name=_name, start_date=_start_date, end_date=_end_date)
        event.save()
        self.events_Owned.append(event)
        self.save()
        return self

    def interests_to_wish(self, _user, _wish):
        """
        Method user to 'wish_back'. i.e signal that tuhe user is interested in the activity.
        :param _user:
        :param _wish:
        :return: self
        """
        user = Users.objects.get(id=_user.id)
        wish = next((w for w in user.wishes if w.wish_id==_wish.wish_id), None)
        wish.add_interested(self)
        self.interested_in.append(wish)
        self.save()
        user.save()
        return self

    def add_media(self, _binaryMedia, _label, _event):
        """
        Method used to add a Media to a users's Media collection
        :param _binaryMedia:
        :return: self
        """
        media = Medias()
        self.medias.append(media)
        self.save()
        return self

    def my_wishes(self):
        return self.wishes





