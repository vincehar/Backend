from upto.models import User, Users, Wishes, UsersRelationships, Events, Preferences
from pymongo import Connection
from rabbitmq import rabbitmq
from django.contrib import auth
import datetime

# Clean users
databaseName = "upto"
connection = Connection(host='127.0.0.1')
collection = connection[databaseName]
users = collection['users']
user = collection['user']
events = collection['events_Owned']

print "------------------------------------------"
print "         clearing Users Collection"
print "------------------------------------------"
user.remove()
users.remove()


for use in ['alex', 'vincent', 'marc']:
    print('create user : ' + use)
    try:
        # password is '123'
        user = User.objects.get(username=use, email='test@bb.com', password='pbkdf2_sha256$20000$3kBOdJ5Y80Au$e6IP7p5VOZCo5p3wvIrFwVcBYoU24ahZ4qwKjhQeOVY=')
    except User.DoesNotExist:
        u=User.objects.create(username=use, email='test2@bb.com', password='pbkdf2_sha256$20000$XEl4EhJOYf1y$iTsb3lMssG+pqj4U7rpFXamt2b5QcHAGNsZ85GJ3/jk=')
        u.save()

        #Creation des queues
        myrabbit = rabbitmq()
        myrabbit.create_connection()
        myrabbit.create_queue(u)
        myrabbit.close()

#Users.objects


marc=Users.objects.get_or_create(user=User.objects.get(username='marc'), preferences=Preferences())
vincent=Users.objects.get_or_create(user=User.objects.get(username='vincent'), preferences=Preferences())
alex=Users.objects.get_or_create(user=User.objects.get(username='alex'), preferences=Preferences())

marc=Users.objects.get(user__username='marc')
vincent=Users.objects.get(user__username='vincent')
alex=Users.objects.get(user__username='alex')
#vincent=Users.objects.get_or_create(user=User.objects.get(username='vincent'), preferences=Preferences())
#alex=Users.objects.get_or_create(user=User.objects.get(username='alex'), preferences=Preferences())


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



marc.create_wish('cine')
marc.create_wish('Je veux voir les etoiles !!!')
marc.create_event(_name='Concert de Johnny !!!', _start_date=datetime.datetime.today(), _end_date=datetime.datetime.today())
marc.create_wish('Je vais coder en python ce soir')
marc.save()

vincent.create_wish('#velo')
vincent.create_wish('Je veux me #reposer ce soir ')
vincent.create_event(_name='Sortie Ski a la Clusaz', _start_date=datetime.datetime.today(), _end_date=datetime.datetime.today())
vincent.create_wish('Je suis chaud pour un #foot')
vincent.save()

alex.create_wish('#alapeche')
alex.create_wish('Qui pour une #raclette')
alex.create_event(_name='Visite du #musee #dimanche', _start_date=datetime.datetime.today(), _end_date=datetime.datetime.today())
alex.create_wish('Je vais coder en python ce soir')
alex.save()

#----------------
#Events part
#----------------
#create_event(self, _name, _startDate, _endDate):


#alex.relate_to_user(marc)


#alex.interests_to_wish(marc, marc.wishes[0])

#alex.accept_follower(vincent)


#marc.make_symerical_relationship(alex)'''