from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^account/$', views.account, name='account'),
    url(r'^wishes/$', views.allwishesAndEvent, name='wishes'),
    url(r'^userdetails/(?P<username>\w+)/$', views.userdetails, name='userdetails')
]
