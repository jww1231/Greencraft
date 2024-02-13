# yourapp/serializers.py

from rest_framework import serializers
from .models import ImageWithText

class ImageWithTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWithText
        fields = ('id', 'car_img', 'bunho_img', 'text')
