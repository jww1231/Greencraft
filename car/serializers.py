from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'displacement', 'name', 'carbon_tax', 'carbon_emission', 'class_label']