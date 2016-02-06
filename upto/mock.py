from upto.models import User, Users, Wishes

for use in ['alex', 'vincent', 'marc']:
    print(use)
    try:
        user = User.objects.get(username=use)
    except User.DoesNotExist:
        u=User.objects.create(username=use)
        u.save()

w=Wishes(title='cine')

us=Users.objects.create(user=User.objects.get(username='marc'))
us.wishes.append(w)
us.save()