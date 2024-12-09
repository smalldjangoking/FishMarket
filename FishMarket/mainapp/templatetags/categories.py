from django import template

from mainapp.models import SeaCategory

register = template.Library()

@register.simple_tag
def categories():
    return SeaCategory.objects.values('name', 'slug')


