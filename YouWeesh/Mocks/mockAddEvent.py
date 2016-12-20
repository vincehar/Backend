from YouWeesh.Models.Users import Users, User
from YouWeesh.Models.Events import Events
from YouWeesh.Models.UsersRelationships import UsersRelationships
from YouWeesh.Models.Preferences import Preferences
from YouWeesh.Models.Coordinates import Coordinates

from pymongo import Connection
#from django.contrib import auth
import datetime

# Connect to DB
databaseName = "upto"
connection = Connection(host='127.0.0.1')
collection = connection[databaseName]
users = collection['users']
user = collection['user']
events = collection['events_Owned']



# - 1 Get ID de Event
ev = Events.objects.get(name='Concert de Johnny !!!')



print "-----------------------------------"
print " Modify Event image                "
print "-----------------------------------"

#user = User.objects.get(username='Anthony', email='test@bb.com', password='pbkdf2_sha256$20000$3kBOdJ5Y80Au$e6IP7p5VOZCo5p3wvIrFwVcBYoU24ahZ4qwKjhQeOVY=')
#antho=Users.objects.get_or_create(user=User.objects.get(username='Anthony'), preferences=Preferences(), current_coordinates=Coordinates(), picture="")



f = open("/home/ubuntu/Pictures/johnny.jpg", "rb")
ev.thumbnail.replace(f)
ev.save()