from upto.models import User, Users, Wishes, UsersRelationships

for use in ['alex', 'vincent', 'marc']:
    print(use)
    try:
        user = User.objects.get(username=use)
    except User.DoesNotExist:
        u=User.objects.create(username=use)
        u.save()


#
usa=Users.objects.get_or_create(user=User.objects.get(username='alex'))
us=Users.objects.get_or_create(user=User.objects.get(username='marc'))
#us[0].save()
#usa[0].save()

alex=Users.objects.get(user=User.objects.get(username='alex'))
marc=Users.objects.get(user=User.objects.get(username='marc'))
marc.create_wish('cine')
marc.save()


alex.relate_to_user(marc)

alex.interests_to_wish(marc, marc.wishes[0])