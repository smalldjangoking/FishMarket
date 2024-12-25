from django.db import models

# Create your models here.

class Cities(models.Model):
    city_name = models.CharField(null=False, blank=False, max_length=155,verbose_name='Город и область')
    ref_to_warehouses = models.CharField(max_length=255, unique=True, verbose_name='Количество отделений')

    def __str__(self):
        return self.city_name

class Warehouses(models.Model):
    city = models.ForeignKey(Cities, null=False, blank=False, to_field='ref_to_warehouses', on_delete=models.CASCADE, related_name='related_warehouses')
    address = models.CharField(null=False, blank=False, max_length=155, verbose_name='Отделение')
    typeofwarehouse = models.IntegerField(null=False, blank=False, verbose_name='Тип отделения')

    def __str__(self):
        return f"{self.address}, {self.city}"