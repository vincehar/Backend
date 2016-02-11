from upto.models import User, Users, Wishes, UsersRelationships, Events
import datetime

for use in ['alex', 'vincent', 'marc']:
    print(use)
    try:
        user = User.objects.get(username=use)
    except User.DoesNotExist:
        u=User.objects.create(username=use)
        u.save()


#
us=Users.objects.get_or_create(user=User.objects.get(username='marc'))
v=Users.objects.get_or_create(user=User.objects.get(username='vincent'))
usa=Users.objects.get_or_create(user=User.objects.get(username='alex'))
#us[0].save()
#usa[0].save()

alex=Users.objects.get(user=User.objects.get(username='alex'))
marc=Users.objects.get(user=User.objects.get(username='marc'))
vincent=Users.objects.get(user=User.objects.get(username='vincent'))
marc.create_wish('cine')
marc.create_wish('Je veux voir les etoiles !!!')
marc.create_wish('Je vais coder en python ce soir')
#create_event(self, _name, _startDate, _endDate):
marc.create_event('Sortie Ski a la Clusaz', datetime.datetime.today(), datetime.datetime.today())
marc.save()
alex.create_wish('Qui pour un sparring en boxe ce soir ?')
alex.save()
vincent.create_wish('Courir au bout du monde !')
vincent.save()






alex.relate_to_user(marc)

vincent.relate_to_user(alex)

alex.interests_to_wish(marc, marc.wishes[0])

alex.accept_follower(vincent)

marc.make_symerical_relationship(alex)