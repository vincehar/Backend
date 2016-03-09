from upto.models import User, Users, Wishes, UsersRelationships, Events
from pymongo import Connection
import datetime

# Clean users
databaseName = "upto"
connection = Connection()
collection = connection[databaseName]
users = collection['users']
events = collection['events_Owned']

print "------------------------------------------"
print "         clearing Users Collection"
print "------------------------------------------"
users.remove()


for use in ['alex', 'vincent', 'marc']:
    print('create user : ' + use)
    try:
        user = User.objects.get(username=use, email='test@bb.com')
    except User.DoesNotExist:
      u=User.objects.create(username=use, email='test2@bb.com')
      u.save()

#Users.objects


us=Users.objects.get_or_create(user=User.objects.get(username='marc'))
v=Users.objects.get_or_create(user=User.objects.get(username='vincent'))
usa=Users.objects.get_or_create(user=User.objects.get(username='alex'))
#us[0].save()
#usa[0].save()

alex=Users.objects.get(user=User.objects.get(username='alex'))
marc=Users.objects.get(user=User.objects.get(username='marc'))
vincent=Users.objects.get(user=User.objects.get(username='vincent'))

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
marc.create_event('Sortie Ski a la Clusaz', datetime.datetime.today(), datetime.datetime.today())
marc.create_wish('Je vais coder en python ce soir')
marc.save()
alex.create_wish('Qui pour un sparring en boxe ce soir ?')
alex.create_event('Aller au concert des 2b3', datetime.datetime.today(), datetime.datetime.today())
alex.save()
vincent.create_wish('Courir au bout du monde !')
vincent.create_event('Particper a la gaypride', datetime.datetime.today(), datetime.datetime.today())
vincent.save()

#----------------
#Events part
#----------------
#create_event(self, _name, _startDate, _endDate):


#alex.relate_to_user(marc)


#alex.interests_to_wish(marc, marc.wishes[0])

#alex.accept_follower(vincent)


#marc.make_symerical_relationship(alex)