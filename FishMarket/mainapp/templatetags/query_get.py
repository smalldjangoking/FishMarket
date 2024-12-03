from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()

    print(request)


    dict_[field] = value

    return dict_.urlencode()
