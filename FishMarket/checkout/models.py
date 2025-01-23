from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_DEFAULT

from mainapp.models import Product
from users.models import User, NovaAddresses, GuestShopper


class Order(models.Model):
    """Model of Order. Created order."""
    class DeliveryOptions(models.TextChoices):
        pending = "1", "Обробляється"
        shipped = "2", "Товар відправлено"
        completed = "3", "Завершено"
        cancelled = "4", "Скасовано"

    PAYMENT_CHOICES = [
        ('1', 'Готівка при отриманні'),
        ('2', 'Оплата на картку')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    guest = models.ForeignKey(GuestShopper, on_delete=models.CASCADE, default=None, null=True, blank=True)
    delivery_address = models.CharField(max_length=255, null=False, blank=False)
    warehouse_number = models.CharField(max_length=255, null=True, blank=True)
    type_of_warehouse = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=DeliveryOptions.choices, default=DeliveryOptions.pending)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)

    def clean(self):
        """Should be a user data for creating an order"""
        if not self.user and not self.guest:
            raise ValidationError("У замовленні має бути або користувач, або гість.")

    def __str__(self):
        if self.user:
            return f"Order {self.id} by {self.user.email}"
        elif self.guest:
            return f"Order {self.id} by guest {self.guest.phone_number}"

class OrderItem(models.Model):
    """Model of Order Items. There is full information about the order item"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=None)
    quantity = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=7, decimal_places=5, null=True, blank=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)

    def clean(self):
        """Customer should choose (buying by quantity that is set or by their chosen weight"""
        if not self.quantity and not self.weight:
            raise ValidationError('Необхідна кількість (quantity) або вага (weight)')


class Payment(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=9, decimal_places=9, null=False, blank=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)