from django.db import models
from django.conf import settings
from car.models import Car

class CarImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='original_images/')
    first_model_image = models.ImageField(upload_to='first_model_images/', null=True, blank=True)
    second_model_image = models.ImageField(upload_to='second_model_images/', null=True, blank=True)
    license_plate_image = models.ImageField(upload_to='license_plate_images/', null=True, blank=True)
    vehicle_type = models.CharField(max_length=200, null=True, blank=True)
    license_plate_text = models.CharField(max_length=200, null=True, blank=True)
    license_plate_vehicle_type = models.CharField(max_length=200, null=True, blank=True)
    g_print = models.TextField(max_length=500, null=True, blank=True)  # Flask 서버로부터 받은 결과물 저장
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
