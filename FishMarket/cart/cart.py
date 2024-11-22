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


    def __len__(self):
        total_quantity = sum(
            int(quantity)
            for product in self.cart.values()
            for quantity in product.get('product_detail').values()
        )
        return total_quantity

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            product = item['product']
            for key, value in item['product_detail'].items():
                if '.' not in key:
                    key = ''
                else:
                    key = Decimal(key)

                yield {
                    'product_weight': key,
                    'product_quantity': int(value),
                    'product_price': int(product.price),
                    'product': product,
                }


    def add(self, product, price, weight=0, quantity=1):
        """
        Addeding products into the cart.
        If weight=0 it is product without any weight. Count by number in stock."""

        product_id = str(product.id)
        product_weight = str(weight)
        product_quantity = str(quantity)
        product_price = str(price)


        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_price': product_price,
                'product_detail': {product_weight: product_quantity}}
        elif product_id in self.cart:
            self.cart[product_id]['product_detail'][product_weight] = product_quantity

        self.session.modified = True


    def get_full_price(self):
        calculation = sum(
            [
                float(item['product_price']) * int(quantity)
                if '.' not in weight
                else float(item['product_price']) * float(weight) * int(quantity)
                for item in self.cart.values()
                for weight, quantity in item['product_detail'].items()
            ])
        return calculation


    def delete_product(self, product_id, product_weight):
        if self.cart[product_id]['product_detail'][product_weight]:
            del self.cart[product_id]['product_detail'][product_weight]

        if not self.cart[product_id]['product_detail']:
            del self.cart[product_id]

        self.session.modified = True