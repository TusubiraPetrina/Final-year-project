from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from api import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView, name='index'),
    
    url(r'^api/farmers/$', views.FarmerBasicView),
    url(r'^api/farmers/(?P<id>[0-9]+)$', views.FarmerDetailView),
    url(r'^api/precipitation/$', views.PreciBasicView),
    url(r'^api/precipitation/(?P<id>[0-9]+)$', views.PreciDetailView),
    url(r'^api/crop/$', views.MaizeBasicView),
    url(r'^api/crop/(?P<type>[a-z]+)$', views.MaizeDetailView),
]


""" urlpatterns += [
    path('catalog/', include('catalog.urls')),
] """

""" urlpatterns += [
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
] """


""" urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) """