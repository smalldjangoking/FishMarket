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
    dict_.pop(field, None)
    print(dict_)
    return dict_.urlencode()

