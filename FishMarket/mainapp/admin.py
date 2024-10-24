from django.contrib import admin

from mainapp.models import SeaCategory, ProductMenu, Product

# Register your models here.

admin.site.register(SeaCategory)
admin.site.register(ProductMenu)
admin.site.register(Product)