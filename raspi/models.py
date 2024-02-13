# models.py
from django.db import models

class ImageWithText(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_img = models.ImageField(upload_to='captured_images/')
    bunho_img = models.ImageField(upload_to='captured_images/')
    text = models.TextField()

    def __str__(self):
        return f"ImageWithText {self.id}"
