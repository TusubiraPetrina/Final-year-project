from rest_framework import serializers
from .models import Farmer, Maize, Precipitation


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = (
            "unique_id",
            "user",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "telephone",
            "region",
            "maize",
            
        )


class MaizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maize
        fields = ("maize_type", "seasonal_price", "production")


class PrecipitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precipitation
        fields = "precipitation_rate"
