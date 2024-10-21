from django.core.exceptions import ValidationError
from django.db import models
from usersapp.models import User


class SeaCategory(models.Model):
    """Model of Categories (Камбала, Вугор, Філе)"""
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, verbose_name='Название Категории')
    image_category = models.ImageField(upload_to='sea_categories', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продукта'


class ProductMenu(models.Model):
    """Model of Product Menu(Камбала в'ялена, Камбала суха...)"""

    name = models.CharField(max_length=30, unique=True, blank=False, null=False, verbose_name='Название подкатегории')
    image_category = models.ImageField(upload_to='product_menu', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    sea_category = models.ForeignKey(SeaCategory, on_delete=models.CASCADE, verbose_name='Категория продукта')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория продукта'
        verbose_name_plural = 'Подкатегории продукта'

class Product(models.Model):
    """Model of Products. Products characteristics are displayed at menu"""
    product_menu = models.ForeignKey(ProductMenu, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image_product = models.ImageField(upload_to='products', blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class ProductWeight(models.Model):
    """Модель для хранения разных весов продукта."""
    status_choices = [
        ('кг', 'Килограммы'),
        ('гр', 'Граммы'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='weights')
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    weight_calculus = models.CharField(choices=status_choices, max_length=50)

    class Meta:
        verbose_name = 'Вес продукта'
        verbose_name_plural = 'Веса продуктов'

    def __str__(self):
        return f"{self.weight} {self.weight_calculus}"

class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    """Model of Order. Created order."""
    status_choices = [
        ('pending', 'Очікується'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status_choices, default='Очікується', max_length=50)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

class OrderItem(models.Model):
    """Model of Order Items. There is full information about the order item"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=7, decimal_places=5, null=True, blank=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=5, null=False, blank=False)

    def clean(self):
        """Customer should choose (buying by quantity that is set or by their chosen weight"""
        if not self.quantity and not self.weight:
            raise ValidationError('Необхідна кількість (quantity) або вага (weight)')

        if self.quantity and self.weight:
            raise ValidationError('Не можна заповнювати одночасно кількість (quantity) і вагу (weight)')


class Payment(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=9, decimal_places=9, null=False, blank=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)