from django import template

from core.utils import get_localized_value

register = template.Library()


@register.filter
def localized(obj, field_name):
    return get_localized_value(
        obj,
        field_name,
    )