from django import template

register = template.Library()


@register.filter
def dict_get(data, key):
    if isinstance(data, dict):
        return data.get(key)
    return None
