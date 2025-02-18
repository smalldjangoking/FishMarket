from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from urllib.parse import urlencode

from users.models import User


class SeaCategory(models.Model):
    """Model of Categories (Камбала, Вугор, Філе)"""
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, verbose_name='Название Категории')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='SLUG_URL')
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
    price = models.IntegerField(verbose_name='Цена за КГ/ШТ')
    stock = models.IntegerField(null=True, blank=True, default=0, verbose_name='Наличие')
    time_create = models.DateTimeField(auto_now_add=True, db_index=True)
    meta_description = models.TextField(
        max_length=160, blank=False, null=False, verbose_name="Meta описание (Для поисковых систем. 160 символ. Уникальность!)")
    meta_tags = models.TextField(blank=True, null=True, verbose_name='Meta Теги (Необязательно. Не больше 10 слов через запятую.)')

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
