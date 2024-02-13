from django.db import models

class Car(models.Model):
    displacement = models.FloatField()  # 배기량
    name = models.CharField(max_length=100)  # 차량명
    carbon_tax = models.DecimalField(max_digits=10, decimal_places=2)  # 탄소세
    carbon_emission = models.FloatField()  # 탄소배출량
    class_label = models.CharField(max_length=50)  # 클래스 라벨

    def __str__(self):
        return self.name
