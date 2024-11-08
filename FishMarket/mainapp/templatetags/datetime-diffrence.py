from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def time_difference(product_time):
    try:
        time_differences = timezone.now() - product_time
        return time_differences.days
    except (ValueError, TypeError):
        return ''