from django.db import models
from django.urls import reverse 
class Maize(models.Model):
    maize_type=models.CharField(primary_key=True,max_length=30)
    seasonal_price=models.DecimalField(verbose_name="seasonal price(UGX)",max_digits=7,decimal_places=2)
    production=models.DecimalField(verbose_name="production(KGs)",max_digits=50,decimal_places=2)
    def __str__(self):
        """String for representing the Model object."""
        return self.maize_type
    def get_absolute_url(self):
        return reverse('maize-detail', args=[str(self.id)])

class Farmer(models.Model):
    
    unique_id = models.CharField(primary_key=True,max_length=10, help_text='Enter your identification number')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telephone=models.IntegerField(help_text='Enter 10 digit phone number')
    region=models.CharField(max_length=50,help_text='Enter region you grow maize')
    maize= models.ManyToManyField(Maize, help_text='Enter maize type')
    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name}, {self.last_name}'
    def get_absolute_url(self):
        return reverse('farmer-detail', args=[str(self.id)])

class Preciptation(models.Model):
    preciptation_rate= models.DecimalField(verbose_name="preciptation rate(mm)",max_digits=5,decimal_places=3)
    def __str__(self):
        """String for representing the Model object."""
        return self.preciptation_rate
    def get_absolute_url(self):
        return reverse('preciptation-detail', args=[str(self.id)])

