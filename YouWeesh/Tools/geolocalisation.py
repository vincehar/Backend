import googlemaps

from YouWeesh.Models.Coordinates import Coordinates
#import responses
from math import sin, cos, sqrt, atan2, radians

class geolocalisation():

    def __init__(self):
        self.key = 'AIzaSyDcRm_4W48Hu4OdwAHSaIfmWerF475RQA0'
        self.client = googlemaps.Client(self.key)
        self.matrixServiceAdress = 'https://maps.googleapis.com/maps/api/distancematrix/json'

    #def getCurrentPosition(self):

    #def getDistance(self):

    def geoCodeWithAddress(self, address):
        coo = Coordinates()
        coo.lat = self.client.geocode(address)[0]['geometry']['location']['lat']
        coo.lng = self.client.geocode(address)[0]['geometry']['location']['lng']
        return coo



    def getDistance(self, _origin, _distination):

        R = 6373.0

        lat1 = radians(_origin.lat)
        lon1 = radians(_origin.lng)
        lat2 = radians(_distination.lat)
        lon2 = radians(_distination.lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance