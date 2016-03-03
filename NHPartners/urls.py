from django.conf.urls import include, url
from django.contrib import admin
from upto import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'NHPartners.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^', include('mongo_auth.contrib.urls')),
    url(r'^upto/', include('upto.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
]
