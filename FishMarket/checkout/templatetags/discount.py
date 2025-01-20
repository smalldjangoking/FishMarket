import decimal

from django import template
from decimal import Decimal, ROUND_HALF_UP

register = template.Library()

@register.simple_tag()
def discount_amount(total, user_discount):
    total = Decimal(total)
    return (total * (user_discount / Decimal('100'))).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

@register.simple_tag()
def price_discounted(total, user_discount):
    total = Decimal(total)
    return (total * (1 - (user_discount / Decimal('100')))).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)