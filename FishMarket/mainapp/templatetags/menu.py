from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def navmenu():
    return {'Головна': {'url': reverse('mainapp:main'), 'class': ''},
            'Продукти': {'url': reverse('mainapp:AllProducts'), 'class': ''},
            'Категорії': {'url': reverse('mainapp:AllProducts'), 'class': 'dropdown'},
            '+38 (098) 8811617': {'url': 'tel: +38 (098) 8811617', 'class': ''},
    }
