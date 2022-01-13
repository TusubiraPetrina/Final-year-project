from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Maize(models.Model):
    maize_type = models.CharField(primary_key=True, max_length=30)
    seasonal_price = models.DecimalField(
        verbose_name="seasonal price(UGX)", max_digits=7, decimal_places=2
    )
    production = models.DecimalField(
        verbose_name="production(KGs)", max_digits=50, decimal_places=2
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.maize_type

    def get_absolute_url(self):
        return reverse("maize-detail", args=[str(self.id)])


class Farmer(models.Model):

    unique_id = models.CharField(primary_key=True, max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="BFarmersUsers")
    username = models.CharField(max_length=100, default="johndoe", help_text="Enter username")
    email = models.EmailField(unique=True, default="test@example.com", help_text="enter your email address")
    first_name = models.CharField(max_length=100, default="John", help_text="Enter first name")
    last_name = models.CharField(max_length=100,default="Doe", help_text="Enter last name")
    is_staff = models.BooleanField(default=False,null=True, blank=True)
    is_active = models.BooleanField(default=False,null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=True, blank=True)
    groups = models.ManyToManyField(User, related_name='FarmerGroups', blank=True)
    user_permissions = models.ManyToManyField(User, related_name='FarmerUserPermissions', blank=True)
    telephone = models.IntegerField(help_text="Enter 10 digit phone number")
    region = models.CharField(max_length=50, help_text="Enter region you grow maize")
    #maize = models.ManyToManyField(Maize, help_text="Enter maize type")

    class Meta:
        ordering = ["first_name", "last_name"]
        #filter_horizontal = ['groups', 'user_permissions']
        #list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
        #list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

    #def __str__(self):
    #    """String for representing the Model object."""
    #    return f"{self.first_name}, {self.last_name}"

    #def get_absolute_url(self):
    #    return reverse("farmer-detail", args=[str(self.id)])


class Precipitation(models.Model):
    preciptation_rate = models.DecimalField(
        verbose_name="precipitation rate(mm)", max_digits=5, decimal_places=3
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.precipitation_rate

    def get_absolute_url(self):
        return reverse("precipitation-detail", args=[str(self.id)])

class Dataset(models.Model):
    year = models.IntegerField()
    production= models.DecimalField(max_digits=10,decimal_places=3)
    precipitation= models.DecimalField(max_digits=10,decimal_places=3)
    price= models.DecimalField(max_digits=10,decimal_places=3)

    def __str__(self):
        """String for representing the Model object."""
        return self.year

class Repository(models.Model):
    username = models.CharField(max_length=50, help_text="Enter username", null=False)
    region = models.CharField(max_length=50, help_text="Enter username", null=False)
    month = models.CharField(max_length=50, help_text="Enter username", null=False)
    production = models.DecimalField(max_digits=10,decimal_places=3, null=False)
    price = models.DecimalField(max_digits=10,decimal_places=3, null=False)
    
    def __str__(self):
        return self.region