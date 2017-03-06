from django.conf.urls import url, include
from upto.regbackend import UsersBackend
from upto.forms import UsersRegistrationForm
import YouWeesh.Controllers.WishController as WishController
import YouWeesh.Controllers.UsersController as UsersController
import YouWeesh.Controllers.LoginController as LoginController
import YouWeesh.Controllers.RegisterController as RegisterController
import YouWeesh.Controllers.EventController as EventController
import YouWeesh.Controllers.LevelControler as LevelControler

from . import views

app_name = 'YouWeesh'
urlpatterns = [
    url(r'^$',views.login, name='index'),
    url(r'^login/$', LoginController.loginUser, name='login'),
    url(r'^getToken/$', LoginController.getToken, name='getToken'),
    url(r'^getTokenForSocialNetwork/$', LoginController.getTokenForSocialNetWork, name='getTokenForSocialNetwork'),
    url(r'^useriscreated/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.useriscreated, name='useriscreated'),
    url(r'^register/', include('regme.urls')),
    url(r'^account/register/', UsersBackend.as_view(form_class=UsersRegistrationForm), name='register'),
    url(r'^account/(?P<_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.account, name='account'),
    url(r'^myevents/$', UsersController.myNextEvents, name='myevents'),
    url(r'^wishes/$', views.allwishesAndEvent, name='wishes'),
    url(r'^getautocompletetags/$', views.getAutoCompleteTags, name='getautocompletetags'),
    url(r'^getweeshbyid/(?P<_wish_id>\w+)/$', WishController.getWeeshById, name='getweeshbyid'),
    url(r'^popupevent/$', views.popUpEvent, name='popupevent'),
    url(r'^geteventbyid/$', views.getEventById, name='geteventbyid'),
    url(r'^getnbrfriends/$', UsersController.getNbrFriends, name='getnbrfriends'),
    url(r'^createwish/$', UsersController.createWish, name='createwish'),
    url(r'^filter/$', UsersController.filter_list, name='filter'),
    url(r'^eventstimeline/$', UsersController.eventsTimeline, name='eventstimeline'),
    url(r'^weeshtimeline/$', UsersController.weeshTimeline, name='weeshtimeline'),
    url(r'^deletewish/(?P<_wish_id>\w+)$', views.deleteWish, name='deletewish'),
    url(r'^createevent/$', UsersController.createEvent, name='createevent'),
    url(r'^uploadpictureuser/$', views.uploadPictureUser, name='uploadpictureuser'),
    url(r'^deleteevent/(?P<_event_id>\w+)$', views.deleteEvent, name='deleteevent'),
    url(r'^event/(?P<_event_id>\w+)/$', views.getEventInfo, name='eventDetails'),
    url(r'^userdetails/(?P<username>\w+)/$', views.userdetails, name='userdetails'),
    url(r'^addfriend/(?P<username>[a-z0-9]+)/$', views.addfriend, name='addfriend'),
    url(r'^acceptfriend/(?P<friend_id>\w+)/$', views.acceptfriend, name='acceptfriend'),
    url(r'^unfriend/(?P<_user_id>\w+)$', views.unfriend, name='unfriend'),
    url(r'^getlevels/$', LevelControler.getLevels, name='getlevels'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^getfavoritetags/(?P<_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.get_favorite_tags, name='getfavoritetags'),
    url(r'^relationships/(?P<username>[a-z0-9]+)/$', views.relationships, name='relationships'),
    #url(r'^testgeoloc/', views.geoloc, name='geoloc'),
    url(r'^savecoordinates/', views.saveCurrentPosition, name='savecoordinates'),
    url(r'^getfriends/(?P<_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', UsersController.getFriends, name='getfriends'),
    #url(r'^login/', views.login, name='login'),
    url(r'^updateposition/', UsersController.updatePosition, name='updateposition'),
    url(r'^allweeshes/$', UsersController.allweeshes, name='allweeshes'),
    url(r'^allevents/$', UsersController.allEvents, name='allevents'),
    url(r'^getweeshbackcount/(?P<_wish_id>\w+)$', WishController.getWeeshBackCount, name='getweeshbackcount'),
    url(r'^weeshback/$', UsersController.weeshback, name='weeshback'),
    url(r'^unweeshback/$', UsersController.unweeshback, name='unweeshback'),
    url(r'^registeruser/$', RegisterController.registeruser, name='registeruser')
]
