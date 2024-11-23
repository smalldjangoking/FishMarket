from django.contrib import admin
from .models import SeaCategory, Product, ProductWeight, ProductImage, MoreInformation
from django.utils.safestring import mark_safe

class ProductWeightInline(admin.TabularInline):
    model = ProductWeight
    extra = 1

class MoreInfo(admin.StackedInline):
    model = MoreInformation
    max_num = 1
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductWeightInline, ProductImageInline, MoreInfo]
    list_display = ('name', 'price', 'stock', 'image_product_show')
    search_fields = ('name',)
    list_filter = ('product_category',)
    prepopulated_fields = {"slug": ("name",)}

    def image_product_show(self, obj):
        if obj.image_product:
            return mark_safe(f"<img src='{obj.image_product.url}' width='60' />")
        return 'None'

    image_product_show.__name__ = 'Изображение товара'

class SeaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_category_show' )
    prepopulated_fields = {"slug": ("name",)}

    def image_category_show(self, obj):
        if obj.image_category:
            return mark_safe(f"<img src='{obj.image_category.url}' width='60' />")
        return 'None'

    image_category_show.__name__ = "Изображение категории"




admin.site.register(SeaCategory, SeaCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.site_header = 'FishMarket | Управление сайтом'

