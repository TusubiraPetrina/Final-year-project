from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from api import views
#from helpers.users import UserList, UserDetails, GroupList


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('', views.IndexView, name='index'),

    #path('auth/' ,include('oauth2_provider.urls', namespace = 'oauth2_provider')),
        
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)