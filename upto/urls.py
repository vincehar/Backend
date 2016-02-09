from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/(?P<nom_user>[a-z]+)/$', views.user_info, name='user_info')
]
