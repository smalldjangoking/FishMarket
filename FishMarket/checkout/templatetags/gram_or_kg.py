from django import template

register = template.Library()

@register.simple_tag
def weight_definition(weight):
    if not weight:
        return ''

    weight = float(weight)
    if weight < 1.000:
        return f"{int(weight * 1000)}г."
    elif weight == 1.000:
        return f"{int(weight)}кг."
    else:
        return f"{round(weight, 1)}кг."