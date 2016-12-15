import datetime
import base64
from YouWeesh.Models.UsersRelationships import UsersRelationships
from YouWeesh.Models.Wishes import Wishes
from YouWeesh.Models.Tags import Tags
from YouWeesh.Models.Events import Events
from YouWeesh.Models.Medias import Medias
from YouWeesh.Models.Preferences import Preferences
from mongoengine.django.auth import User
from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
from bson import ObjectId


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
    current_coordinates = EmbeddedDocumentField('Coordinates')
    #friends = ListField(ReferenceField('UsersRelationships'))
    #wishes = ListField(ReferenceField('Wishes'))
    #logs = ListField(ReferenceField('Logs'))
    #messages = ListField(EmbeddedDocumentField('Messages'))
    #categories_Selected = ListField(EmbeddedDocumentField('Categories'))
    #medias = ListField(ReferenceField('Medias'))
    #events_Owned = ListField(ReferenceField('Events'))
    #interested_in = ListField(ReferenceField('Wishes'))


    def get_position(self):
        """
        Return formatted position
        #{ "lat" : 46.1954229 , "lng" : 6.1552161 }
        :return:
        """
        return "{'lat': "+ str(self.current_coordinates.lat) +", 'lng':"+ str(self.current_coordinates.lat)+"}"

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

    def create_wish(self, _title, _level):
        """
        Method used to create a wish
        :param _title:
        :param _creation_date:
        :return: self
        """

        wish = Wishes(user_id=self.id, title=_title, creation_date=datetime.datetime.now(), level=_level)

        splitTitle = _title.split(' ')
        for word in splitTitle:
            if word.startswith('#'):
                tag = Tags.objects.get_or_create(title=word)
                wish.tags.append(tag[0])

        wish.save()
        return wish

    def create_event(self, **kwargs):

        if 'thumbnail' in kwargs:
            event = Events(user_id=self.id, name=kwargs['eventName'], start_date=kwargs['start_date'], end_date=kwargs['end_date'], thumbnail=kwargs['thumbnail'], creation_date=datetime.datetime.now())
        else:
            event = Events(user_id=self.id, name=kwargs['eventName'], start_date=kwargs['start_date'], end_date=kwargs['end_date'], creation_date=datetime.datetime.now())

        splitTitle = kwargs['eventName'].split(' ')
        for word in splitTitle:
            if word.startswith('#'):
                tag = Tags.objects.get_or_create(title=word)
                event.tags.append(tag[0])
        event.save()
        #Connect and send message to the queue
        # Use plain credentials for authentication

        #mqueue.publish_message('coco', 'New weesh created', channel, 'amq_fanout')
        #mqueue.close(connection)

        return event

    def interests_to_wish(self, _user, _wish):
        user = Users.objects.get(id=_user.id)
        wish = next((w for w in user.wishes if w.id==_wish.id), None)
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
        # TODO : Test is null
        if self.picture:
            picture = base64.b64encode(self.picture.read())
            return picture
        else:
            return None

