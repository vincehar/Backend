from django.conf.urls import url

from . import views

app_name = 'upto'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^account/$', views.account, name='account'),
    url(r'^wishes/$', views.allwishesAndEvent, name='wishes'),
    url(r'^createwish/$', views.createWish, name='createwish'),
    url(r'^createevent/$', views.createEvent, name='createevent'),
    url(r'^event/(?P<_event_id>\w+)/$', views.getEventInfo, name='eventDetails'),
    url(r'^userdetails/(?P<username>[a-z]+)/$', views.userdetails, name='userdetails')
]
