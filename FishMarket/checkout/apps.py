from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    verbose_name = 'Заказы'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
