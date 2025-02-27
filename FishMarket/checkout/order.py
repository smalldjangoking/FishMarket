from decimal import Decimal

from django.db import transaction
from cart.cart import Cart
from cart.templatetags.total_per_product import total_per_product
from checkout.models import Order, OrderItem
from checkout.templatetags.discount import price_discounted
from users.models import NovaAddresses, GuestShopper



def create_order(cleaned_data):
    name = cleaned_data.get('name')
    last_name = cleaned_data.get('last_name')
    phone = cleaned_data.get('phone')
    type_of_delivery = cleaned_data.get('delivery_type', None)
    address = cleaned_data.get('user_address', None)
    payment_method = cleaned_data.get('payment_type', None)
    address_from_memory = cleaned_data.get('address_from_memory', None)
    request = cleaned_data.get('request', None)
    cart = Cart(request)
    user_discount = request.user.discount

    if address_from_memory:
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                delivery_address=address,
                cart_total=price_discounted(cart.get_full_price(), Decimal(user_discount)) if user_discount else cart.get_full_price(),
                payment_method=payment_method,
            )
            order_items_create(cart=cart, order=order)

            return True

    if not address_from_memory:
        with transaction.atomic():
            if request.user.is_authenticated:
                order = Order.objects.create(user=request.user, cart_total=cart.get_full_price(), delivery_address=address, payment_method=payment_method)
                order_items_create(cart=cart, order=order)
                NovaAddresses.objects.create(user=request.user, delivery_choice=type_of_delivery, delivery_address=address)
                return True
            else:
                guest = GuestShopper.objects.create(name=name, last_name=last_name, phone_number=phone)
                order = Order.objects.create(guest=guest, cart_total=cart.get_full_price(), delivery_address=address, payment_method=payment_method)
                order_items_create(cart=cart, order=order)
                return True

    return False




def save_user_info(user, name, last_name, phone):
    if not user.name:
        user.name = name
    if not user.last_name:
        user.last_name = last_name
    if not user.phone_number:
        user.phone_number = phone

    user.save()


def save_user_delivery(user, type_of_delivery, delivery_address, warehouse_number):
    NovaAddresses.objects.create(
        user=user,
        delivery_address=delivery_address,
        warehouse_id=warehouse_number,
        delivery_choice=type_of_delivery,
    )


def create_guest_shopper(name, last_name, phone):
    guest = GuestShopper.objects.create(
        name=name,
        last_name=last_name,
        phone_number=phone
    )

    return guest


def order_items_create(cart, order):
    for product in cart:
        quantity = int(product.get('product_quantity'))
        weight = product.get('product_weight') if product.get('product_weight') not in [None,
                                                                                               ""] else False
        price = float(product.get('product_price'))

        OrderItem.objects.create(
            order=order,
            product=product.get('product'),
            quantity=quantity,
            weight=weight,
            total_price=total_per_product(price_per_kg=price, weight_per_unit=weight, quantity=quantity),
        )

    else:
        cart.cart_clear()

