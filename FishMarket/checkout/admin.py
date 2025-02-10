from django.contrib import admin
from checkout.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = ('quantity', 'weight', 'total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('user_or_guest', 'payment_method', 'delivery_address', 'total_product_item_price', 'created_at')
    list_display = ('__str__', 'status', 'created_at')
    list_editable = ('status',)
    exclude = ("guest", 'user')
    ordering = ('status',)
    search_fields = ('id',)
    list_filter = ('status',)
    list_per_page = 15
    inlines = (OrderItemInline,)

    def user_or_guest(self, obj):
        if obj.guest:
            return f'Гость: {obj.guest}'
        if obj.user:
            return f'Пользователь: {obj.user}'

    def total_product_item_price(self, obj):
        total = sum(item.total_price for item in obj.order_items.all())
        return f'{total} грн'

    user_or_guest.short_description = "Покупатель"
    total_product_item_price.short_description = 'Общая Сумма заказа'