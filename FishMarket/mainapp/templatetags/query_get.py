from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def url_delete(request, field):
    dict_ = request.GET.copy()
    if field == 'min_price':
        del dict_[field]
        del dict_['max_price']
    else:
        dict_.pop(field, None)
    return dict_.urlencode()

@register.simple_tag
def request_tags(request):
    translate = {
        'ASC': 'ціна від меншої до більшої',
        'DESC': 'ціна від більшої до меншої'
    }

    dict_ = request.GET.copy()
    dict_changed = {}

    if not dict_:
        return dict_changed

    min_price = dict_.pop('min_price', [None])[0]
    max_price = dict_.pop('max_price', [None])[0]
    sort = dict_.pop('sort', [None])[0]
    pagination = dict_.pop('page', None)
    if min_price and max_price:
        dict_changed['min_price'] = f'від {min_price} грн до {max_price} грн'

    if sort:
        dict_changed['sort'] = translate[sort]


    for name, value in dict_.items():
        dict_changed[name] = value

    return dict_changed



