from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^account/$', views.account, name='account'),
    url(r'^wishes/$', views.allwishesAndEvent, name='wishes'),
    url(r'^event/(?P<_event_id>\w+)/$', views.getEventInfo, name='eventDetails'),
    url(r'^account/(?P<nom_user>[a-z]+)/$', views.user_info, name='user_info')
]
