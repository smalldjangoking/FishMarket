from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from django.db.models import Prefetch, Q
from checkout.models import Order, OrderItem
import re


def id_search(id_value):
    """Извлекает числовое значение из строки, возвращает 0, если чисел нет."""
    number = ''.join([number for number in id_value if number.isdigit()])

    if number:
        return number
    else:
        return 0


def phone_rebuilder(phone_value):
    """Преобразует строку в формат номера телефона (+38(XXX)-XXX-XX-XX), возвращает '1111111111' при некорректном вводе."""
    digits = re.sub(r'[^0-9]', '', phone_value)

    if len(digits) == 12 and digits.startswith('38'):
        return f"+38({digits[2:5]})-{digits[5:8]}-{digits[8:10]}-{digits[10:12]}"
    elif len(digits) == 10:
        return f"+38({digits[0:3]})-{digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    return '1111111111'


def get_full_name(order):
    """Возвращает полное имя и фамилию пользователя или гостя, связанного с заказом."""
    return order.user.name + ' ' + order.user.last_name if order.user else order.guest.name + ' ' + order.guest.last_name


def get_phone_number(order):
    """Возвращает номер телефона пользователя или гостя, связанного с заказом."""
    return order.user.phone_number if order.user else order.guest.phone_number


def is_paid(order):
    """Строка для prepare_order_message_and_keyboard"""
    check = "✅"
    red_square = "🟥"

    return (check + '\nОПЛАЧЕНО') if order.is_paid else (red_square + '\nНЕ ОПЛАЧЕНО')


def inline_main_kb(order):
    """Клавиатура для отображения меню ордера"""
    inline_kb = InlineKeyboardBuilder()
    if not order.is_paid:
        inline_kb.row(
            InlineKeyboardButton(
                text='Установить как "Заказ Оплачен" ✅',
                callback_data=f'order_{order.id}_is_paid'))

    inline_kb.row(InlineKeyboardButton(
        text='Изменить Статус Заказа 🔄',
        callback_data=f'order_{order.id}_{order.status}_status'))

    return inline_kb


def prepare_order_message_and_keyboard(order):
    """Подготавливает текст сообщения и клавиатуру для отображения информации"""
    inline_kb = inline_main_kb(order)

    order_items = ''
    for item in order.order_items.all():
        order_items += (f'<b>Продукт:</b> <i>{item.product.name}</i>\n'
                        f'Кол: <i>{item.quantity}</i> | Вес: <i>{item.weight}</i> | Всего: <i>{item.total_price}</i>\n')

    order_sting = (f'<b>Заказ №</b>{order.id} \n\n'
                   f'<b>Адрес доставки</b> 🚚\n<i>{order.delivery_address}</i>\n'
                   f'<b>Получатель</b> 👤\n<i>{get_full_name(order)}</i>\n'
                   f'<b>Номер телефона</b> 📱\n<i>{get_phone_number(order)}</i>\n\n'
                   f'<b>Способ оплаты</b> 💳\n<i>{order.get_payment_method_display()}</i>\n'
                   f'<b>Сумма заказа</b> 💸\n<i>{order.cart_total} грн</i>\n'
                   f'<b>Статус оплаты</b> <i>{is_paid(order)}</i>\n\n'
                   f'<b>Заказ Создан</b> 🕔 \n<i>{order.created_at.strftime("%d.%m.%Y %H:%M")}</i>\n'
                   f'<b>Статус Заказа</b> 🔄 \n<i>{order.get_status_display()}</i>\n\n'
                   f'<b>Заказ</b> 🛒\n'
                   f'<blockquote expandable>{order_items}</blockquote>\n')

    return order_sting, inline_kb


def get_kb_from_order(order_id, current_status):
    """Создаем клавиатуру для выбора статуса заказа."""
    DeliveryOptions = Order.DeliveryOptions.choices

    builder = InlineKeyboardBuilder()

    for status_value, status_label in DeliveryOptions:
        if status_value != current_status:
            builder.row(InlineKeyboardButton(
                text=status_label,
                callback_data=f"set_status_{order_id}_status_{status_value}_{status_label}_status_label"
            ))
    builder.row(InlineKeyboardButton(
        text='Назад ⬅️',
        callback_data=f"set_status_{order_id}_{current_status}_status_exit"
    ))

    return builder


@sync_to_async
def get_orders_queryset(search_input):
    """Получает список заказов по поисковому запросу (телефон или ID) с оптимизированными запросами."""
    phone = phone_rebuilder(search_input)

    orders = Order.objects.filter(Q(guest__phone_number__icontains=phone) |
                                  Q(user__phone_number__icontains=phone) | Q(id=id_search(search_input)),
                                  status__in=[1, 2]
                                  ).select_related("user", 'guest').prefetch_related(
        Prefetch('order_items', queryset=OrderItem.objects.select_related('product')))

    return [order for order in orders]


@sync_to_async
def get_order_by_id(order_id):
    """Получает один заказ по ID с оптимизированными запросами."""

    order = Order.objects.filter(id=order_id, status__in=[1, 2]) \
        .select_related("user", "guest") \
        .prefetch_related(
        Prefetch('order_items',
                 queryset=OrderItem.objects.select_related('product'))
    ).first()

    return order

@sync_to_async
def get_orders_queryset_all(status_id):
    """Получает список заказов всех что в обработке или отправленные с птимизированными запросами."""

    orders = Order.objects.filter(status=status_id
                                  ).select_related("user", 'guest').prefetch_related(
        Prefetch('order_items', queryset=OrderItem.objects.select_related('product')))

    return [order for order in orders]


def test(order_id):
    """Получает один заказ по ID с оптимизированными запросами."""

    order = Order.objects.filter(id=order_id, status__in=[1, 2]) \
        .select_related("user", "guest") \
        .prefetch_related(
        Prefetch('order_items',
                 queryset=OrderItem.objects.select_related('product'))
    ).first()

    return order
