from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def navmenu():
    return {'Головна': reverse('mainapp:main'), 'Доставка': reverse('mainapp:delivery'),
            'Контакти': '#', '+38 (098) 8811617': 'tel:+1234567890', }