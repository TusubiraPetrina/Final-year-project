from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Dataset, Farmer, Maize, Precipitation, Repository

class FarmerInline(admin.StackedInline):
    model = Farmer
    can_delete = False
    verbose_name = 'Farmer'
    verbose_name_plural = 'Farmers'

# Define a new User admin
class FarmerAdmin(admin.ModelAdmin):
    inlines = []

# Register your models here.
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Maize)
admin.site.register(Precipitation)
admin.site.register(Dataset)
admin.site.register(Repository)
