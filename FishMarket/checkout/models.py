from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_DEFAULT

from mainapp.models import Product
from users.models import User, NovaAddresses, GuestShopper


class Order(models.Model):
    """Model of Order. Created order."""
    class DeliveryOptions(models.TextChoices):
        pending = "1", "Обробляється"
        shipped = "2", "Відправлено"
        completed = "3", "Завершено"
        cancelled = "4", "Скасовано"

    PAYMENT_CHOICES = [
        ('1', 'Готівка при отриманні'),
        ('2', 'Оплата на картку')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    guest = models.ForeignKey(GuestShopper, on_delete=models.CASCADE, default=None, null=True, blank=True)
    delivery_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес Доставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=1, choices=DeliveryOptions.choices, default=DeliveryOptions.pending, verbose_name='Статус Заказа')
    payment_method = models.CharField(blank=False, null=False , max_length=1, choices=PAYMENT_CHOICES, verbose_name='Метод оплаты')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    cart_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Сумма за все товары')


    def clean(self):
        """Should be a user data for creating an order"""
        if not self.user and not self.guest:
            raise ValidationError("У замовленні має бути або користувач, або гість.")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f"Заказ {self.id} Пользователь: {self.user.phone_number}"
        elif self.guest:
            return f"Заказ {self.id} Гость: {self.guest.phone_number}"

class OrderItem(models.Model):
    """Model of Order Items. There is full information about the order item"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=None, verbose_name='Продукт')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Количество')
    weight = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Выбранный вес')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, verbose_name='Сумма за товар')

    def clean(self):
        """Customer should choose (buying by quantity that is set or by their chosen weight"""
        if not self.quantity and not self.weight:
            raise ValidationError('Необхідна кількість (quantity) або вага (weight)')