from rest_framework import serializers
from .models import Farmer, Maize, Precipitation,Dataset, Repo


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields='__all__'


class MaizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maize
        fields='__all__'


class PrecipitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precipitation
        fields='__all__'

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        # fields =['year', 'price', 'production','precipitation']
        fields='__all__'

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        # fields =['year', 'price', 'production','precipitation']
        fields='__all__'
