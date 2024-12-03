from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def navmenu():
    return {'Головна': reverse('mainapp:main'), 'Продукти': reverse('mainapp:AllProducts'),
            'Доставка': reverse('mainapp:delivery'), '+38 (098) 8811617': 'tel:+1234567890', }
