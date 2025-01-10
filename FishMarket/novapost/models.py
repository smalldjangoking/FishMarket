from django.db import models

# Create your models here.

class Cities(models.Model):
    city_name_ua = models.CharField(null=False, blank=False, max_length=155,verbose_name='Город UA')
    city_name_ru = models.CharField(null=False, blank=False, max_length=155, verbose_name='Город RU')
    city_state = models.CharField(null=False, blank=False, max_length=155, verbose_name='Область')
    ref_to_warehouses = models.CharField(max_length=255, unique=True, verbose_name='Количество отделений')

    def __str__(self):
        return self.city_name_ua

class Warehouses(models.Model):
    city = models.ForeignKey(Cities, null=False, blank=False, to_field='ref_to_warehouses', on_delete=models.CASCADE, related_name='related_warehouses')
    number = models.IntegerField(null=False, blank=False)
    address_ua = models.CharField(null=False, blank=False, max_length=155, verbose_name='Адрес UA')
    address_ru = models.CharField(null=True, blank=True, max_length=155, verbose_name='Адрес RU')
    typeofwarehouse = models.IntegerField(null=False, blank=False, verbose_name='Тип отделения')

    def __str__(self):
        return f"{self.address}, {self.city}"