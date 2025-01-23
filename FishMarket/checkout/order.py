import logging
from decimal import Decimal

from django.db import transaction

from cart.cart import Cart
from cart.templatetags.total_per_product import total_per_product
from checkout.models import Order, OrderItem
from users.models import NovaAddresses, GuestShopper, User


def create_order(cleaned_data):
    user = cleaned_data.get('user_id', None)
    name = cleaned_data.get('name')
    last_name = cleaned_data.get('last_name')
    phone = cleaned_data.get('phone')
    type_of_delivery = cleaned_data.get('type_of_delivery')
    courier_delivery = cleaned_data.get('courier_delivery', None)
    warehouse_delivery = cleaned_data.get('delivery_address', None)
    warehouse_number = cleaned_data.get('warehouse_number', None)
    payment_method = cleaned_data.get('payment', None)
    request = cleaned_data.get('request', None)
    cart = Cart(request)

    if warehouse_delivery and warehouse_number:
        delivery_address = warehouse_delivery
    else:
        delivery_address = (f'м. {courier_delivery["city"]}, '
                            f'вул. {courier_delivery["street"]}, '
                            f'буд. {courier_delivery["house"]}'
                            f'{", кв. " + courier_delivery["apartment"] if courier_delivery.get("apartment", None) is not None else ""}')

    if user is None:
        guest = create_guest_shopper(name, last_name, phone)

    try:
        with transaction.atomic():
            order = Order.objects.create(
                user=User.objects.get(id=int(user)) if user is not None else None,
                guest=guest if user is None else None,
                delivery_address=delivery_address,
                warehouse_number=warehouse_number,
                type_of_warehouse=type_of_delivery,
                payment_method=payment_method,
            )

            for product in cart:
                quantity = int(product.get('product_quantity'))
                weight = float(product.get('product_weight')) if product.get('product_weight') not in [None,
                                                                                                       ""] else None
                price = float(product.get('product_price'))

                OrderItem.objects.create(
                    order=order,
                    product=product.get('product'),
                    quantity=quantity,
                    weight=weight,
                    total_price=total_per_product(price, weight, quantity),
                )

            cart.cart_clear()

        return True

    except Exception as e:
        logging.error(e)
        return False



def save_user_address(cleaned_data):
    user = cleaned_data.get("user_id")
    type_of_delivery = cleaned_data.get("type_of_delivery")
    warehouse_number = cleaned_data.get("warehouse_number")
    delivery_address = cleaned_data.get("delivery_address")
    NovaAddresses.objects.create(
        user=user,
        delivery_choice=type_of_delivery,
        warehouse_id=warehouse_number,
        warehouse_address=delivery_address
    )


def create_guest_shopper(name, last_name, phone):
    guest = GuestShopper.objects.create(
        name=name,
        last_name=last_name,
        phone=phone
    )

    return guest
