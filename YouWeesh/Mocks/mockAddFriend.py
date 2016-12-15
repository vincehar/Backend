from YouWeesh.Models.Users import Users, User
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


print "-----------------------------------"
print "Create Relationships - add friends"
print "-----------------------------------"

# - 1 Get ID de Marc
marc = Users.objects.get(user__username='marc')
# - 2 Get ID de Vincent
vincent = Users.objects.get(user__username='vincent')


UsersRelationships.objects.get_or_create(from_user=marc.id, to_user=vincent.id, accepted=True)


print "-----------------------------------"
print "Create User                        "
print "-----------------------------------"

#user = User.objects.get(username='Anthony', email='test@bb.com', password='pbkdf2_sha256$20000$3kBOdJ5Y80Au$e6IP7p5VOZCo5p3wvIrFwVcBYoU24ahZ4qwKjhQeOVY=')
#antho=Users.objects.get_or_create(user=User.objects.get(username='Anthony'), preferences=Preferences(), current_coordinates=Coordinates(), picture="")

# 1 - insert picture on DB
f = open("/home/ubuntu/Pictures/profil.jpeg", "rb")
vincent.picture.replace(f)
vincent.save()


f = open("/home/ubuntu/Pictures/profil.jpeg", "rb")
marc.preferences.background_picture.replace(f)
marc.save()