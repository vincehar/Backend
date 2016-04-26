from django.core.mail.backends.console import EmailBackend
from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine.django.auth import User
#from regme.documents import User
from rabbitmq import rabbitmq
import pika
import datetime
import base64
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
from bson import ObjectId


class Wishes(Document):
    user_id = ReferenceField('Users')
    wish_id = ObjectIdField(default=ObjectId)
    title = StringField(required=True)
    creation_date = DateTimeField(default=datetime.datetime.now())
    interested = ListField(ReferenceField('Users'))
    tags = ListField(ReferenceField('Tags'))

    def user_name(self):
        return self.user_id.username

    def get_ref_date(self):
        return self.creation_date

    def add_interested(self, user):
        self.interested.append(user)


class Tags(Document):
    title = StringField(required=True)


class Logs(Document):
    user_id = ReferenceField('Users')
    ip_address = StringField(required=True)
    date = DateTimeField(required=True)
    action = StringField(required=True)


class Categories(EmbeddedDocument):
    name = StringField(required=True)

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
    interested = ListField(ReferenceField('Users'))
    event_id = ObjectIdField(default=ObjectId)
    name = StringField(required=True)
    thumbnail = ImageField()
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    address = EmbeddedDocumentField('Address')
    creation_date = DateTimeField(default=datetime.datetime.now())
    price = FloatField()
    #devise = models
    categories = ListField(EmbeddedDocumentField('Categories'))
    eventStatus = EmbeddedDocumentField('EventStatus')


    def get_ref_date(self):
        return self.creation_date

    def get_picture(self):
        thumbnail = base64.b64encode(self.thumbnail.read())
        return thumbnail

class Messages(Document):
    from_user = ReferenceField('Users')
    to_user = ReferenceField('Users')
    creation_date = DateTimeField()
    content = BinaryField()
    event = EmbeddedDocumentField('Events')


class Album(EmbeddedDocument):
    name = StringField(required=True)

class Medias(Document):
    content = BinaryField()
    label = StringField()
    event = EmbeddedDocumentField('Events', required=True)
    album = EmbeddedDocumentField('Album')

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

class Preferences(EmbeddedDocument):
    display_weeshes = BooleanField(default=True)
    display_events = BooleanField(default=True)
    search_distance = IntField(default=50)
    selected_network = StringField(default='PUBLIC')

class Users(Document):
    """
    Main class representing the Users entities.
    This is the class in which everything is embedded.
    """
    user_id = ObjectIdField(default=ObjectId)
    user = EmbeddedDocumentField('User')
    picture = ImageField()
    preferences = EmbeddedDocumentField('Preferences')
    date_created = DateTimeField(default=datetime.datetime.now())
    #friends = ListField(ReferenceField('UsersRelationships'))
    #wishes = ListField(ReferenceField('Wishes'))
    #logs = ListField(ReferenceField('Logs'))
    #messages = ListField(EmbeddedDocumentField('Messages'))
    #categories_Selected = ListField(EmbeddedDocumentField('Categories'))
    #medias = ListField(ReferenceField('Medias'))
    #events_Owned = ListField(ReferenceField('Events'))
    #interested_in = ListField(ReferenceField('Wishes'))

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
        rel = UsersRelationships(from_user=self, to_user=user, accepted=False, blocked=False)
        rel.save()
        return self

    def accept_follower(self, _users):
        """
        Method used to activate a relationship, i.e accept a follower
        :param user:
        :return:
        """

        self.save()
        return self

    def add_friend(self, _users):
        """

        :return:
        """
        relation = UsersRelationships(from_user=self, to_user=_users, accepted=False)
        relation.save()
        return self

    def create_wish(self, _title):
        """
        Method used to create a wish
        :param _title:
        :param _creation_date:
        :return: self
        """

        wish = Wishes(user_id=self.id, title=_title, creation_date=datetime.datetime.now())

        splitTitle = _title.split(' ')
        for word in splitTitle:
            if word.startswith('#'):
                tag = Tags.objects.get_or_create(title=word)
                wish.tags.append(tag[0])

        wish.save()

        #Connect and send message to the queue
        # Use plain credentials for authentication
        myrabbit = rabbitmq()
        myrabbit.create_connection()
        myrabbit.publish_newweesh(wish.wish_id,wish.user_id.user.username)
        myrabbit.close()
        return wish

    def create_event(self, **kwargs):

        if 'thumbnail' in kwargs:
            event = Events(user_id=self.id, name=kwargs['eventName'], start_date=kwargs['start_date'], end_date=kwargs['end_date'], thumbnail=kwargs['thumbnail'], creation_date=datetime.datetime.now())
        else:
            event = Events(user_id=self.id, name=kwargs['eventName'], start_date=kwargs['start_date'], end_date=kwargs['end_date'], creation_date=datetime.datetime.now())
        event.save()

        #Connect and send message to the queue
        # Use plain credentials for authentication
        myrabbit = rabbitmq()
        myrabbit.create_connection()
        myrabbit.publish_newevent(event.event_id, event.user_id.user.username)
        myrabbit.close()
        #mqueue.publish_message('coco', 'New weesh created', channel, 'amq_fanout')
        #mqueue.close(connection)

        return event

    def interests_to_wish(self, _user, _wish):
        user = Users.objects.get(id=_user.id)
        wish = next((w for w in user.wishes if w.wish_id==_wish.wish_id), None)
        wish.add_interested(self)
        self.interested_in.append(wish)
        self.save()
        user.save()
        return self

    def add_media(self, _binaryMedia, _label, _event):
        media = Medias()
        self.medias.append(media)
        self.save()
        return self

    def my_wishes(self):
        return self.wishes

    def get_picture(self):
        picture = base64.b64encode(self.picture.read())
        return picture











