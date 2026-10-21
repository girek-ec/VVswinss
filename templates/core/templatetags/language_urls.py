from django import template
from django.urls import translate_url


register = template.Library()


@register.simple_tag(takes_context=True)
def language_url(context, language_code):
    request = context.get("request")

    if request is None:
        return "/"

    return translate_url(
        request.get_full_path(),
        language_code,
    )