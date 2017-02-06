from mongoengine import EmbeddedDocument, FloatField, Document, EmbeddedDocumentField, \
    ReferenceField, StringField, ListField, DateTimeField, BinaryField, BooleanField, ObjectIdField, ImageField, IntField
from YouWeesh.Models.Coordinates import Coordinates
from YouWeesh.Tools.geolocalisation import geolocalisation

class Address(EmbeddedDocument):
    address_1 = StringField(default="")
    address_2 = StringField(default="")
    city = StringField(default="")
    state = StringField(default="")
    zip_code = StringField(default="")
    current_coordinates = EmbeddedDocumentField('Coordinates')

    def getorUpdateCoordinates(self):
        if (self.address_1 != "" or self.address_2 != "") and (self.city != "" or self.zip_code != ""):
            geo = geolocalisation()
            print(self.address_1 +" "+ self.address_2 + ", " + self.city + " " + self.zip_code)
            self.current_coordinates = geo.geoCodeWithAddress(str(self.address_1)+" "+ str(self.address_2) + ", " + str(self.city) + " " + str(self.zip_code))
