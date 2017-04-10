from django.conf.urls import url, include
from upto.regbackend import UsersBackend
from upto.forms import UsersRegistrationForm
import YouWeesh.Controllers.WishController as WishController
import YouWeesh.Controllers.UsersController as UsersController
import YouWeesh.Controllers.LoginController as LoginController
import YouWeesh.Controllers.RegisterController as RegisterController
import YouWeesh.Controllers.EventController as EventController
import YouWeesh.Controllers.LevelControler as LevelControler
import YouWeesh.Controllers.SportsController as SportsController

from . import views

app_name = 'YouWeesh'
urlpatterns = [
    url(r'^$',views.login, name='index'),
    url(r'^login/$', LoginController.loginUser, name='login'),
    url(r'^getToken/$', LoginController.getToken, name='getToken'),
    url(r'^getTokenForSocialNetwork/$', LoginController.getTokenForSocialNetWork, name='getTokenForSocialNetwork'),
    url(r'^useriscreated/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.useriscreated, name='useriscreated'),
    url(r'^updatepicture/$', UsersController.updatepicture, name='updatepicture'),
    url(r'^updatebackgroundpicture/$', UsersController.updatebackgroundpicture, name='updatebackgroundpicture'),
    url(r'^account/register/', UsersBackend.as_view(form_class=UsersRegistrationForm), name='register'),
    url(r'^account/(?P<_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.account, name='account'),
    url(r'^myevents/$', UsersController.myNextEvents, name='myevents'),
    url(r'^getweeshbyid/(?P<_wish_id>\w+)/$', WishController.getWeeshById, name='getweeshbyid'),
    url(r'^geteventbyid/(?P<_event_id>\w+)$', EventController.getEventById, name='geteventbyid'),
    url(r'^getsports/(?P<searchterm>\w+)$', SportsController.getsports, name='getsports'),
    url(r'^getnbrfriends/$', UsersController.getNbrFriends, name='getnbrfriends'),
    url(r'^createwish/$', UsersController.createWish, name='createwish'),
    url(r'^filter/$', UsersController.filter_list, name='filter'),
    url(r'^eventstimeline/$', UsersController.eventsTimeline, name='eventstimeline'),
    url(r'^weeshtimeline/$', UsersController.weeshTimeline, name='weeshtimeline'),
    url(r'^deletewish/(?P<_wish_id>\w+)$', views.deleteWish, name='deletewish'),
    url(r'^createevent/$', UsersController.createEvent, name='createevent'),
    url(r'^addfriend/$', UsersController.addfriend, name='addfriend'),
    url(r'^acceptfriend/(?P<friend_id>\w+)/$', views.acceptfriend, name='acceptfriend'),
    url(r'^addparticipant/$', EventController.addParticipant, name='addparticipant'),
    url(r'^deleteparticipant/$', EventController.deleteParticipant, name='deleteparticipant'),
    url(r'^getlevels/$', LevelControler.getLevels, name='getlevels'),
    url(r'^getfavoritetags/(?P<_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.get_favorite_tags, name='getfavoritetags'),
    url(r'^getfriends/(?P<_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.getFriends, name='getfriends'),
    url(r'^updateposition/', UsersController.updatePosition, name='updateposition'),
    url(r'^allweeshes/$', UsersController.allweeshes, name='allweeshes'),
    url(r'^allevents/$', UsersController.allEvents, name='allevents'),
    url(r'^getweeshbackcount/(?P<_wish_id>\w+)$', WishController.getWeeshBackCount, name='getweeshbackcount'),
    url(r'^weeshback/$', UsersController.weeshback, name='weeshback'),
    url(r'^unweeshback/$', UsersController.unweeshback, name='unweeshback'),
    url(r'^registeruser/$', RegisterController.registeruser, name='registeruser')
]
