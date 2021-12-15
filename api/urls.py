from django.urls import path, include
from django.conf.urls import url
from helpers.users import UserList, UserDetails, GroupList
#from helpers.login import CustomAuthToken
from .views import *

urlpatterns = [
    #path('login/', CustomAuthToken.as_view()),
    
    #path('users/', UserList.as_view()),
    #path('users/<id>', UserDetails.as_view()),
    #path('groups/', GroupList.as_view()),

    path('', include('helpers.urls')), 

    url(r'^farmers/$', FarmerBasicView),
    url(r'^farmers/(?P<id>[0-9]+)$', FarmerDetailView),
    url(r'^precipitation/$', PreciBasicView),
    url(r'^precipitation/(?P<id>[0-9]+)$', PreciDetailView),
    url(r'^crop/$', MaizeBasicView),
    url(r'^crop/(?P<type>[a-z]+)$', MaizeDetailView),
]