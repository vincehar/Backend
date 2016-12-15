from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
import base64

class Preferences(EmbeddedDocument):
    display_weeshes = BooleanField(default=True)
    display_events = BooleanField(default=True)
    search_distance = IntField(default=50)
    selected_network = StringField(default='PUBLIC')
    background_picture = ImageField()


    def get_background_picture(self):
        # TODO : Test is null
        if self.background_picture:
            picture = base64.b64encode(self.background_picture.read())
            return picture
        else:
            return None