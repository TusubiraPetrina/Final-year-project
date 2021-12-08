from django.contrib import admin

# Register your models here.
from .models import Farmer,Maize,Preciptation
admin.site.register(Farmer)
admin.site.register(Maize)
admin.site.register(Preciptation)


