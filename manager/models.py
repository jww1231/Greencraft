from django.db import models

class BusinessCode(models.Model):
    managercode = models.CharField(max_length=20, unique=True)  # 사업자코드
    address = models.CharField(max_length=100)  # 주소
    gasoline_price = models.DecimalField(max_digits=5, decimal_places=2)  # 휘발유 가격
    phone_number = models.CharField(max_length=15)  # 전화번호
    pump_number = models.IntegerField()  # 주유기 번호

    def __str__(self):
        return self.managercode
