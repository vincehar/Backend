import googlemaps
from YouWeesh.Models.Coordinates import Coordinates
from datetime import datetime
#import responses

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



    def getDistance(self):
       # responses.add(responses.GET,
        #              self.matrixServiceAdress,
         #             body='{"status":"OK","rows":[]}',
          #            status=200,
           #           content_type='application/json')

        # sample adresses
        origins = [{ "lat" : 46.1954229 , "lng" : 6.1552161 }] #["8 place Camoletti, 1205 Geneve"]
        destinations = ["28 Rue Des contamines, 1206 Geneve"]

        matrix = self.client.distance_matrix(origins, destinations)
        return matrix

    def test(self, _string):
        return _string