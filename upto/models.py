from django.db import models as orimodels
#from mongo_auth.contrib.models import User
from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine.django.auth import User
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField
from bson import ObjectId

class Wishes(EmbeddedDocument):
    wish_id = ObjectIdField(default=ObjectId)
    title = StringField(required=True)
    interested = ListField(ReferenceField('Users'))

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

class Events(Document):
    name = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    address = StringField()
    price = FloatField()
    #devise = models
    categories = ListField(EmbeddedDocumentField('Categories'))
    eventStatus = EmbeddedDocumentField('EventStatus')

class Album(EmbeddedDocument):
    name = StringField(required=True)

class Medias(Document):
    content = BinaryField()
    label = StringField()
    event = EmbeddedDocumentField('Events', required=True)
    album = EmbeddedDocumentField('Album')

class UsersRelationships(EmbeddedDocument):
    from_user = ReferenceField('Users')
    to_user = ReferenceField('Users')
    active = BooleanField()
    symetrical = BooleanField()
    blocked = BooleanField()

    def make_symetrical(self):
        """
        Method used to make a relationship symetrical, i.e user a follows back user b.
        :return: self
        """
        self.symetrical=True
        self.save()
        return self

class Users(Document):
    """
    Main class representing the Users entities.
    This is the class in which everything is embedded.
    """
    user = EmbeddedDocumentField('User')
    wishes = ListField(EmbeddedDocumentField('Wishes'))
    logs = ListField(EmbeddedDocumentField('Logs'))
    friends = ListField(EmbeddedDocumentField('UsersRelationships'))
    messages = ListField(EmbeddedDocumentField('Messages'))
    categories_Selected = ListField(EmbeddedDocumentField('Categories'))
    medias = ListField(EmbeddedDocumentField('Medias'))
    events_Owned = ListField(EmbeddedDocumentField('Events'))
    Interested_in = ListField(EmbeddedDocumentField('Wishes'))

    def relate_to_user(self, user):
        """
        Method used to relate to another user, i.e follow a user.
        :param user: instance of Users class
        :return: self
        """
        rel= UsersRelationships(from_user=self, to_user=user, active=False, symetrical=False, blocked=False)
        self.friends.append(rel)
        self.save()
        return self

    def make_symerical_relationship(self, user):
        """
        Method used to follow a user that already follows you, i.e follow back a user.
        :param user: instance of Users class
        :return: self
        """
        rel = UsersRelationships.objects.get(from_user=user, to_user=self)
        rel.make_symetrical()
        self.save()
        return self

    def create_wish(self, _title):
        wish = Wishes(title=_title)
        self.wishes.append(wish)
        self.save()
        return self

    def interests_to_wish(self, _user, _wish):
        user = Users.objects.get(id=_user.id)
        wish = next((w for w in user.wishes if w.wish_id==_wish.wish_id), None)
        wish.add_interested(self)
        self.Interested_in.append(wish)
        self.save()
        user.save()
        return self

