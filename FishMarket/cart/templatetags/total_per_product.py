from django import template

register = template.Library()


@register.simple_tag()
def total_per_product(price_per_kg, weight_per_unit, quantity):
    if not weight_per_unit:
        return float(price_per_kg * quantity)
    else:
        return price_per_kg * weight_per_unit * quantity
