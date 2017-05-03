import base64

from mongoengine import EmbeddedDocument, StringField, BooleanField, ImageField, \
    IntField


class Preferences(EmbeddedDocument):
    display_weeshes = BooleanField(default=True)
    display_events = BooleanField(default=True)
    search_distance = IntField(default=50)
    search_string = StringField(default='')
    selected_network = StringField(default='PUBLIC')
    background_picture = ImageField()

    def get_background_picture(self):
        if self.background_picture:
            picture = base64.b64encode(self.background_picture.read())
            return picture
        else:
            return None
