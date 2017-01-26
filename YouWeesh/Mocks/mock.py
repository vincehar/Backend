from YouWeesh.Models.Users import Users, User
from YouWeesh.Models.Events import Events
from YouWeesh.Models.Preferences import Preferences
from YouWeesh.Models.Tags import Tags
from YouWeesh.Models.Coordinates import Coordinates
from YouWeesh.Models.Wishes import Wishes
from YouWeesh.Models.Level import Level

from pymongo import Connection
#from django.contrib import auth
import datetime

# Clean users
databaseName = "upto"
connection = Connection(host='127.0.0.1')
collection = connection[databaseName]
users = collection['users']
user = collection['user']
events = collection['events']
wishes = collection['wishes']
level = collection['level']
tags = collection['tags']


print "------------------------------------------"
print "         clearing Users Collection"
print "------------------------------------------"
user.remove()
users.remove()
wishes.remove()
level.remove()
tags.remove()
events.remove()


for use in ['alex', 'vincent', 'marc']:
    print('create user : ' + use)
    try:
        # password is '123'
        user = User.objects.get(username=use, email='test@bb.com', password='pbkdf2_sha256$20000$3kBOdJ5Y80Au$e6IP7p5VOZCo5p3wvIrFwVcBYoU24ahZ4qwKjhQeOVY=')
    except User.DoesNotExist:
        u=User.objects.create(username=use, email='test2@bb.com', password='pbkdf2_sha256$20000$XEl4EhJOYf1y$iTsb3lMssG+pqj4U7rpFXamt2b5QcHAGNsZ85GJ3/jk=')
        u.save()

#Users.objects

lvl = Level()
lvl2 =  Level()
lvl3 =  Level()
lvl4 =  Level()
coo = Coordinates()

lvl.idLevel = 0
lvl.description = 'Beginner'
lvl.save()

lvl2.idLevel = 1
lvl2.description = 'Initiated'
lvl2.save()

lvl3.idLevel = 2
lvl3.description = 'Confirmed'
lvl3.save()

lvl4.idLevel = 3
lvl4.description = 'Expert'
lvl4.save()
print coo.lat

marc=Users.objects.get_or_create(user=User.objects.get(username='marc'), preferences=Preferences(), current_coordinates=coo)
vincent=Users.objects.get_or_create(user=User.objects.get(username='vincent'), preferences=Preferences(), current_coordinates=coo)
alex=Users.objects.get_or_create(user=User.objects.get(username='alex'), preferences=Preferences(), current_coordinates=coo)



marc=Users.objects.get(user__username='marc')
vincent=Users.objects.get(user__username='vincent')
alex=Users.objects.get(user__username='alex')
#vincent=Users.objects.get_or_create(user=User.objects.get(username='vincent'), preferences=Preferences())
#alex=Users.objects.get_or_create(user=User.objects.get(username='alex'), preferences=Preferences())

# Rue des Contamines, 1206 GENEVE
vincent.current_coordinates.lat = 46.1954229
vincent.current_coordinates.lng = 6.1552161
vincent.save()

#Creation des queues
#myrabbit = rabbitmq()
#myrabbit.create_connection()
#myrabbit.create_queue(marc)
#myrabbit.create_queue(vincent)
#myrabbit.create_queue(alex)
#myrabbit.close()

#us[0].save()
#usa[0].save()
#----------------
#Make relationship
#----------------
#alex.relate_to_user(marc)
#alex.relate_to_user(vincent)

#----------------
#Wishes part
#----------------
#f = open("/home/ubuntu/PycharmProjects/NHPartners/YouWeesh/Mocks/Pictures/sportback.jpeg", "rb")
#marc.preferences.background_picture.replace(f)
#marc.save()


marc.create_wish('Match de #Basket dans le coin ?', lvl)
marc.create_wish('A fond chaud pour un sparing de #Boxe', lvl)
marc.create_event(eventName='#Trail des Roussets !',start_date=datetime.datetime.today(), end_date=datetime.datetime.today())

ev = Events.objects.get(title='#Trail des Roussets !')
f = open("/home/ubuntu/PycharmProjects/NHPartners/YouWeesh/Mocks/Pictures/trail.jpg", "rb")
ev.thumbnail.replace(f)
ev.save()

marc.create_wish('Du #velo ce week-end qui est chaud ?', lvl)
marc.save()

vincent.create_wish('#Cycling', lvl)
vincent.create_wish('Un #futsal organise cette semaine ?', lvl)
vincent.create_event(eventName='Sortie #Ski a la Clusaz', start_date=datetime.datetime.today(), end_date=datetime.datetime.today())
ev = Events.objects.get(title='Sortie #Ski a la Clusaz')
f = open("/home/ubuntu/PycharmProjects/NHPartners/YouWeesh/Mocks/Pictures/ski.jpg", "rb")
ev.thumbnail.replace(f)
ev.save()
vincent.create_wish('Je suis chaud pour un #trail', lvl)
vincent.save()

alex.create_wish('Je propose un #tennis a un 30-4 ou niveau equivalent', lvl)
alex.create_wish('Quelqu un connait une salle de #muscu sympa ?', lvl)
alex.create_event(eventName='#Futsal du dimanche', start_date=datetime.datetime.today(), end_date=datetime.datetime.today())
ev = Events.objects.get(title='#Futsal du dimanche')
f = open("/home/ubuntu/PycharmProjects/NHPartners/YouWeesh/Mocks/Pictures/futsal.jpg", "rb")
ev.thumbnail.replace(f)
ev.save()
alex.create_wish('Depart de Geneve pour du #ski, quelqu un', lvl)
alex.save()

f = open("/home/ubuntu/PycharmProjects/NHPartners/YouWeesh/Mocks/Pictures/sportback.jpeg", "rb")
marc.preferences.background_picture.replace(f)
marc.save()

#----------------
#Events part
#----------------
#create_event(self, _name, _startDate, _endDate):


#alex.relate_to_user(marc)


#alex.interests_to_wish(marc, marc.wishes[0])

#alex.accept_follower(vincent)


#marc.make_symerical_relationship(alex)'''