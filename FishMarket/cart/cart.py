from decimal import Decimal
from django.conf import settings
from mainapp.models import Product


class Cart():
    """Bucket list class. For addeding products, deleting, updating and count quantity for bucket banner"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        print(self.cart)

    def __len__(self):
        total_quantity = sum(
            int(quantity)
            for product in self.cart.values()
            for quantity in product.get('product_detail').values()
        )
        return total_quantity

    def add(self, product, price, weight=0, quantity=1):
        """
        Addeding products into the cart.
        If weight=0 it is product without any weight. Count by number in stock."""

        product_id = str(product.id)
        product_weight = str(weight)
        product_price = str(price)
        product_quantity = str(quantity)


        if product_id not in self.cart:
            self.cart[product_id] = {'product_detail': {product_weight: product_quantity}}
            self.cart[product_id].setdefault('product_price', product_price)
        elif product_id in self.cart:
            self.cart[product_id]['product_detail'][product_weight] = product_quantity

        self.session.modified = True


