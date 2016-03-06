from django.conf.urls import url, include
from upto.regbackend import UsersBackend
from upto.forms import UsersRegistrationForm

from . import views

app_name = 'upto'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', include('regme.urls')),
    url(r'^account/register/', UsersBackend.as_view(form_class=UsersRegistrationForm), name='register'),
    url(r'^account/$', views.account, name='account'),
    url(r'^wishes/$', views.allwishesAndEvent, name='wishes'),
    url(r'^createwish/(?P<username>[a-z0-9]+)/$', views.createWish, name='createwish'),
    url(r'^deletewish/(?P<_wish_id>\w+)$', views.deleteWish, name='deletewish'),
    url(r'^createevent/$', views.createEvent, name='createevent'),
    url(r'^deleteevent/(?P<_event_id>\w+)$', views.deleteEvent, name='deleteevent'),
    url(r'^event/(?P<_event_id>\w+)/$', views.getEventInfo, name='eventDetails'),
    url(r'^userdetails/(?P<username>[a-z0-9]+)/$', views.userdetails, name='userdetails'),
    url(r'^login/', views.login, name='login'),
]
