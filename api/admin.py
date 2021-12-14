from django.contrib import admin

# Register your models here.
from .models import Farmer,Maize,Precipitation
admin.site.register(Farmer)
admin.site.register(Maize)
admin.site.register(Precipitation)


