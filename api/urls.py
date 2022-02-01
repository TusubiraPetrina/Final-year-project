from django.urls import path, include
from django.conf.urls import url
from helpers.users import UserList, UserDetails, GroupList

# from helpers.login import CustomAuthToken
from .views import *

urlpatterns = [
    path("", include("helpers.urls")),
    url(r"^farmers/$", FarmerBasicView),
    path("farmers/<str:id>/", FarmerDetailView),
    url(r"^precipitation/$", PreciBasicView),
    url(r"^precipitation/(?P<id>[0-9]+)$", PreciDetailView),
    url(r"^crop/$", MaizeBasicView),
    url(r"^crop/(?P<type>[a-z]+)$", MaizeDetailView),
    url(r"^dataset/$", dataset),
    path('dataset/<int:year>/', dataByYear),
    url(r"^repository/$", RepositoryView),
]
