# from rest_framework import serializers
# from .models import CarImage
# from django.contrib.auth.models import User
# from django.conf import settings
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = settings.AUTH_USER_MODEL
#         fields = ['id', 'username']
#
# class CarImageSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)  # 사용자 정보 포함
#
#     class Meta:
#         model = CarImage
#         fields = ['id', 'user', 'original_image', 'first_model_image', 'second_model_image', 'license_plate_image', 'vehicle_type', 'license_plate_text', 'license_plate_vehicle_type']