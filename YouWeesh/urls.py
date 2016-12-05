from django.conf.urls import url, include
from upto.regbackend import UsersBackend
from upto.forms import UsersRegistrationForm
import YouWeesh.Controllers.WishController as WishController
import YouWeesh.Controllers.UsersController as UsersController
import YouWeesh.Controllers.EventController as EventController

from . import views

app_name = 'YouWeesh'
urlpatterns = [
    url(r'^$',views.login, name='index'),
    url(r'^register/', include('regme.urls')),
    url(r'^account/register/', UsersBackend.as_view(form_class=UsersRegistrationForm), name='register'),
    url(r'^account/$', UsersController.account, name='account'),
    url(r'^myevents/$', UsersController.myNextEvents, name='myevents'),
    url(r'^wishes/$', views.allwishesAndEvent, name='wishes'),
    #url(r'^weeshesevents/$', views.weeshesevents, name='weeshesevents'),
    url(r'^getautocompletetags/$', views.getAutoCompleteTags, name='getautocompletetags'),
    url(r'^getweeshbyid/$', WishController.getWeeshById, name='getweeshbyid'),
    url(r'^popupevent/$', views.popUpEvent, name='popupevent'),
    url(r'^geteventbyid/$', views.getEventById, name='geteventbyid'),
    url(r'^createwish/$', views.createWish, name='createwish'),
    url(r'^filter/$', views.filter_list, name='filter'),
    url(r'^deletewish/(?P<_wish_id>\w+)$', views.deleteWish, name='deletewish'),
    url(r'^createevent/$', views.createEvent, name='createevent'),
    url(r'^uploadpictureuser/$', views.uploadPictureUser, name='uploadpictureuser'),
    url(r'^deleteevent/(?P<_event_id>\w+)$', views.deleteEvent, name='deleteevent'),
    url(r'^event/(?P<_event_id>\w+)/$', views.getEventInfo, name='eventDetails'),
    url(r'^userdetails/(?P<username>\w+)/$', views.userdetails, name='userdetails'),
    url(r'^addfriend/(?P<username>[a-z0-9]+)/$', views.addfriend, name='addfriend'),
    url(r'^acceptfriend/(?P<friend_id>\w+)/$', views.acceptfriend, name='acceptfriend'),
    url(r'^unfriend/(?P<_user_id>\w+)$', views.unfriend, name='unfriend'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^relationships/(?P<username>[a-z0-9]+)/$', views.relationships, name='relationships'),
    #url(r'^testgeoloc/', views.geoloc, name='geoloc'),
    url(r'^savecoordinates/', views.saveCurrentPosition, name='savecoordinates'),
    url(r'^getfriends/', UsersController.getFriends, name='getfriends'),
    #url(r'^login/', views.login, name='login'),
]
