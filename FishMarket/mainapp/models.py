from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from urllib.parse import urlencode

from usersapp.models import User


class SeaCategory(models.Model):
    """Model of Categories (Камбала, Вугор, Філе)"""
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, verbose_name='Название Категории')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='SLUG_URL')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Описание Категории')
    image_category = models.ImageField(upload_to='sea_categories', blank=True, null=True, verbose_name='Титульная картинка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія продукту'
        verbose_name_plural = 'Категорії продукту'

    def get_absolute_url(self):
        base_url = reverse('mainapp:AllProducts')
        query = urlencode({'category': self.slug})
        return f'{base_url}?{query}'


class Product(models.Model):
    """Model of Products. Products characteristics are displayed at menu"""
    product_category = models.ForeignKey(SeaCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='SLUG_URL')
    image_product = models.ImageField(upload_to='products', blank=False, null=False, verbose_name='Титульная картинка')
    description = models.TextField(verbose_name='Описание Продукта')
    price = models.IntegerField(verbose_name='Цена за КГ')
    stock = models.IntegerField(null=True, blank=True, default=0, verbose_name='Наличие')
    time_create = models.DateTimeField(auto_now_add=True, db_index=True)
    meta = models.CharField(max_length=140, blank=True, default='')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'
        ordering = ['time_create']

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mainapp:product', kwargs={'slug': self.slug})



class ProductWeight(models.Model):
    """Модель для хранения разных весов продукта."""
    status_choices = [
        ('кг', 'Килограммы'),
        ('гр', 'Граммы'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='weights')
    weight = models.DecimalField(max_digits=6, decimal_places=3, db_index=True)
    weight_calculus = models.CharField(choices=status_choices, max_length=50)

    class Meta:
        verbose_name = 'Вес продукта'
        verbose_name_plural = 'Веса продуктов'

    def __str__(self):
        return f"{self.weight} {self.weight_calculus}"


class ProductImage(models.Model):
    """Модель для хранения дополнительных фотографий продукта."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='product_images')

    class Meta:
        verbose_name = 'Дополнительная фотография продукта'
        verbose_name_plural = 'Дополнительные фотографии продуктов'

    def __str__(self):
        return f"Фото для {self.product.name}"


class MoreInformation(models.Model):
    """Модель для хранения хароктеристик продукта и его свойствах."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='information')
    region = models.CharField(max_length=40, verbose_name='Регіон походження')
    ingredients = models.CharField(max_length=100, verbose_name='Інгредієнти')
    packing = models.CharField(max_length=100, verbose_name='Упаковка')
    weight_difference = models.CharField(max_length=100, verbose_name='Різниця у вагах')
    salt_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Солоність')
    shelf_life = models.CharField(max_length=100, verbose_name='Час зберігання')



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