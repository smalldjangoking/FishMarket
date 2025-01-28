import logging
from decimal import Decimal

from django.db import transaction
import json
from cart.cart import Cart
from cart.templatetags.total_per_product import total_per_product
from checkout.models import Order, OrderItem
from users.models import NovaAddresses, GuestShopper, User


def create_order(cleaned_data):
    user = cleaned_data.get('user_id', None)
    name = cleaned_data.get('name')
    last_name = cleaned_data.get('last_name')
    phone = cleaned_data.get('phone')
    type_of_delivery = int(cleaned_data.get('type_of_delivery'))
    courier_delivery = cleaned_data.get('courier', None)
    warehouse_delivery = cleaned_data.get('delivery_address', None)
    warehouse_number = cleaned_data.get('warehouse_number', None)
    payment_method = cleaned_data.get('payment', None)
    request = cleaned_data.get('request', None)
    cart = Cart(request)

    if type_of_delivery == '1':
        delivery_address = warehouse_delivery
    else:
        courier_delivery = json.loads(courier_delivery)
        delivery_address = \
            (f'м. {courier_delivery["city"]}, вул. {courier_delivery["street"]}, буд. {courier_delivery["house"]} '
             f'{", кв. " + courier_delivery["apartment"] if courier_delivery["apartment"] else ""}')

    if user is None:
        guest = create_guest_shopper(name, last_name, phone)
    else:
        user = User.objects.get(id=int(user))
        save_user_info(user, name, last_name, phone)
        print('начинаем')
        save_user_delivery(user, type_of_delivery, delivery_address, warehouse_number)

    try:
        with transaction.atomic():
            order = Order.objects.create(
                user=user if user is not None else None,
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
